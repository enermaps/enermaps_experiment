#!/usr/bin/env python3
"""This import a simple raster into the geoserver
"""
import requests
import argparse
import os


def post(user, password):
    url = "http://localhost:8000/geoserver/rest/imports?async=true"
    payload = {
       "import": {
          "targetWorkspace": {
             "workspace": {
            "name": "topp"
             }
          },
          "data": {
            "type": "remote",
            "location": "ftp://myserver/data/bc_shapefiles",
            "username": "dan",
            "password": "secret"
          }
       }
    }
    requests.get(url, auth=(user, password), json=payload)


def get_parser():
    """return the cli command parser
    """
    parser = argparse.ArgumentParser(__name__, description="import a raster into a geoserver")
    parser.add_argument("-u", "--user", default="geoserver")
    parser.add_argument("shapefile")
    return parser


def main():
    print("importing raster")

    parser = get_parser()
    args = parser.parse_args()
    post(user=args.user, password=os.environ['GEOSERVER_PASS'])

if __name__ == "__main__":
    main()
