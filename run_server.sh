#!/bin/bash

gunicorn minimal-mvt-aiohttp:app -b localhost:8081 -w 1 --worker-class aiohttp.GunicornUVLoopWebWorker
