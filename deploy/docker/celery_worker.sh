#!/bin/bash
celery -A polling_api.core.celery worker -l info --without-gossip --without-mingle -Q polling_api
