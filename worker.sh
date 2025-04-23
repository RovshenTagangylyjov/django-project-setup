#!/bin/bash

# email worker
celery -A config worker -l debug --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo --concurrency 1 --queues email &

# For other tasks
celery -A config worker -l debug --concurrency 3 --queues celery &

# periodic task scheduler
celery -A config beat -l debug
