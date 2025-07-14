import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import httpx
from fastapi import FastAPI

USERS_API_SCHEMA_URL = os.getenv('USERS_API_SCHEMA_URL', 'http://localhost:8000/gateway/auth/api/schema/')
POLLING_API_SCHEMA_URL = os.getenv('USERS_API_SCHEMA_URL', 'http://localhost:8000/gateway/polling/api/v1/openapi.json')


class OpenApiMerger:
    def __init__(self) -> None:
        self._merged_spec: dict = {}

    @property
    def merged_spec(self) -> dict:
        return self._merged_spec

    @staticmethod
    def _default_headers() -> dict:
        return {
            'Accept': 'application/json',
        }

    async def fetch_spec(self, url: str) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=self._default_headers())
            response.raise_for_status()
            return response.json()

    async def refresh(self) -> None:
        users_api_spec = await self.fetch_spec(USERS_API_SCHEMA_URL)
        polling_api_spec = await self.fetch_spec(POLLING_API_SCHEMA_URL)

        merged = {
            'openapi': '3.0.3',
            'info': {'title': 'Unified API', 'version': '1.0'},
            'paths': {},
            'components': {},
        }

        merged['paths'].update(users_api_spec.get('paths', {}))
        merged['paths'].update(polling_api_spec.get('paths', {}))

        merged['components'] = users_api_spec.get('components', {})
        for key, val in polling_api_spec.get('components', {}).items():
            merged['components'].setdefault(key, {}).update(val)

        self._merged_spec = merged


merger = OpenApiMerger()


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator:
    await merger.refresh()
    yield


app_configs: dict[str, Any] = {
    'title': 'Gateway API',
    'description': 'Universal Gateway API',
    'debug': False,
}

app = FastAPI(**app_configs, lifespan=lifespan)


def get_merged_openapi():
    return merger.merged_spec


app.openapi = get_merged_openapi


@app.get('/ht/', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}
