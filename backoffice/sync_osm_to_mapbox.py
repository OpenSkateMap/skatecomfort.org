#!/usr/bin/env python3

import logging
import os
import overpass
import requests

QUERY='way["skating_comfort"]'
MAPBOX_USER='anticristi'
MAPBOX_TILESET_ID='skating_comfort'
MAPBOX_ACCESS_TOKEN=os.environ['MAPBOX_ACCESS_TOKEN']

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('sync_osm_to_mapbox')

logger.info('Loading skating_comfort from OSM')
api = overpass.API(timeout=60)
response = api.get(QUERY, responseformat="geojson", verbosity='geom')

logger.info('Got %d features', len(response["features"]))

geoJsonLd = '\n'.join([ str(feature) for feature in response['features'] ])
logger.info('Writing debug.geojson.ld')
open('debug.geojson.ld', 'w').write(geoJsonLd)

logger.info('Replacing Mapbox tileset source')

# We use the same tileset source ID as the tileset ID.
url = f'https://api.mapbox.com/tilesets/v1/sources/{MAPBOX_USER}/{MAPBOX_TILESET_ID}'
params = { 'access_token': MAPBOX_ACCESS_TOKEN }
files = { 'file': geoJsonLd }

r = requests.put(
    url = url,
    params = params,
    files = files,
)
logger.info('Got response with status_code %s', r.status_code)
logger.info('Got response with body %s', r.json())

logger.info('Publishing new tileset')
url = f'https://api.mapbox.com/tilesets/v1/{MAPBOX_USER}.{MAPBOX_TILESET_ID}/publish'
params = { 'access_token': MAPBOX_ACCESS_TOKEN }
r = requests.post(
    url = url,
    params = params,
)
logger.info('Got response with status_code %s', r.status_code)
logger.info('Got response with body %s', r.json())
