
# Client setup

```
cd map-openlayers/
npm install
```

# Server Setup

```
cd minimal-mvt
virtualenv --python python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

The tile server requires one of these options:

- Aa database connection (postgres) for `minimal-mvt.py` or `minimal-mvt-aiohttp-pg.py` server versions.

- mbtiles file for `minimal-mvt-aiohttp-mbtiles.py` server.

# Configuration of the original `minimal-mvt.py` server:

You'll find the config settings at the beggining of the script.

# Run

#### Client:

`./run_client.sh`

#### Server (only for aiohttp versions):

`./run_server.sh [pg|mbtiles]`