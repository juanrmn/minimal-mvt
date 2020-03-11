#!/bin/bash

case "$1" in
pg)
    . .venv/bin/activate
    gunicorn minimal-mvt-aiohttp-pg:app -b localhost:8081 -w 1 --worker-class aiohttp.GunicornUVLoopWebWorker
;;
mbtiles)
    . .venv/bin/activate
    gunicorn minimal-mvt-aiohttp-mbtiles:app -b localhost:8081 -w 1 --worker-class aiohttp.GunicornUVLoopWebWorker
;;
esac