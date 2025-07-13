#!/bin/bash
celery -A twitch_polling_api.core.celery worker -l info --without-gossip --without-mingle -Q twitch_polling_api
