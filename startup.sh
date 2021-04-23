#!/bin/bash
docker container run --rm -d -p 8000:80 -v $(pwd)/local.env:/app/local.env hungoncloud/uq_notifier:latest
