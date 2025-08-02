import asyncio
import json

import redis.asyncio as redis
from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse

redis_client = redis.StrictRedis(host='redis', decode_responses=True)


async def event_stream(request):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('sse_channel')

    while True:
        if await request.is_disconnected():
            break
        message = await pubsub.get_message()
        if message:
            print(message)
            yield f'data: {message["data"]}\n\n'
        await asyncio.sleep(0.1)


async def send_event(data) -> None:
    await redis_client.publish('sse_channel', json.dumps(data))


event_router = APIRouter()


@event_router.get('/gateway/polling/sse/')
async def sse_events(request: Request):
    return StreamingResponse(event_stream(request), media_type='text/event-stream')
