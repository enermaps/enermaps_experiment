#!/usr/bin/env python3
"""This import a simple raster into the geoserver
"""
import requests
import argparse
import os


def post(user, password, file_path):
    url = "http://localhost:8000/geoserver/rest/imports"
    payload = {"import": {"targetWorkspace": {"workspace": {"name": "enermaps"}}}}
    session = requests.Session()
    session.auth = (user, password)
    resp = session.post(url, json=payload)
    print(resp, resp.text)
    resp_payload = resp.json()
    import_id = resp_payload["import"]["id"]

    filename = os.path.basename(file_path)
    url = "http://localhost:8000/geoserver/rest/imports/{!s}/tasks".format(import_id)
    with open(file_path) as shapefile:
        resp = session.post(url, files={"name": filename, "filedata": shapefile})
        print(resp, resp.text)
    resp = session.post(
        "http://localhost:8000/geoserver/rest/imports/{!s}".format(import_id)
    )
    print(resp, resp.text)


def get_parser():
    """return the cli command parser
    """
    parser = argparse.ArgumentParser(
        __name__, description="import a raster into a geoserver"
    )
    parser.add_argument("-u", "--user", default="admin")
    parser.add_argument("shapefile")
    return parser


def main():
    print("importing raster")

    parser = get_parser()
    args = parser.parse_args()
    post(
        user=args.user, password=os.environ["GEOSERVER_PASS"], file_path=args.shapefile
    )


if __name__ == "__main__":
    main()
