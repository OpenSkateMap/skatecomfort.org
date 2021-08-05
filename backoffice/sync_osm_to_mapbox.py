#!/usr/bin/env python3

import logging
import os
import overpass
import requests

QUERY='way["skating_comfort"]'
MAPBOX_USER='anticristi'
MAPBOX_TILESET_ID='ckrxgep2805sv21oja37n658t-9k84g'
MAPBOX_ACCESS_TOKEN=os.environ['MAPBOX_ACCESS_TOKEN']

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('sync_osm_to_mapbox')

logger.info('Loading skating_comfort from OSM')
api = overpass.API()
response = api.get(QUERY, responseformat="geojson")

logger.info('Got %d features', len(response["features"]))

geoJsonLd = '\n'.join([ str(feature) for feature in response['features'] ])
for line in geoJsonLd.splitlines():
    logger.debug('Feature: %s', line)

logger.info('Replacing Mapbox tileset')

# $ curl -X PUT "https://api.mapbox.com/tilesets/v1/sources/anticristi/hello-world?access_token=YOUR MAPBOX ACCESS TOKEN
# This endpoint requires a token with tilesets:write scope.
#  " \
#     -F file=@/Users/username/data/mts/countries.geojson.ld \
#     --header "Content-Type: multipart/form-data"
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
