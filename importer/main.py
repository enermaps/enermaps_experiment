#!/usr/bin/env python3
"""This import a simple raster into the geoserver
"""
import argparse
import logging
import os
import posixpath
from collections import defaultdict

import requests

nested_dict = lambda: defaultdict(nested_dict)
NestedDict = nested_dict()


class GeoserverImportError(Exception):
    pass


DATASTORE = {"dataStore": {"name": "geoserver_db"}}


def get_import_creation_payload(workspace_name):
    import_creation_payload = NestedDict
    import_creation_payload["import"]["targetWorkspace"]["workspace"][
        "name"
    ] = workspace_name
    import_creation_payload["targetStore"] = DATASTORE
    return import_creation_payload


def import_file(base_url, user, password, file_path, workspace_name, is_raster=False):
    session = requests.Session()
    session.auth = (user, password)
    import_creation_payload = get_import_creation_payload(workspace_name)
    url = posixpath.join(base_url, "rest/imports")
    resp = session.post(url, json=import_creation_payload)
    if not resp.ok:
        raise GeoserverImportError(resp.text)
    resp_payload = resp.json()
    import_id = resp_payload["import"]["id"]

    filename = os.path.basename(file_path)
    url = posixpath.join(base_url, "rest/imports/{!s}/tasks".format(import_id))
    with open(file_path, "br") as shapefile:
        resp = session.post(url, files={"name": filename, "filedata": shapefile})
        logging.info(resp, resp.text)
        if not resp.ok:
            raise GeoserverImportError(resp.text)

    if not is_raster:
        # the file doesn't have a store set, so it will default to the default store
        # currently we don't support importing raster file to postgis directly
        url = posixpath.join(
            base_url, "rest/imports/{!s}/tasks/0/target".format(import_id)
        )
        resp = session.put(url, json=DATASTORE)
        if not resp.ok:
            raise GeoserverImportError(resp.text)
        logging.info(resp, resp.text)

    url = posixpath.join(base_url, "rest/imports/{!s}".format(import_id))
    resp = session.post(url)
    if not resp.ok:
        raise GeoserverImportError(resp.text)
    logging.info(resp, resp.text)


def get_parser():
    """return the cli command parser"""
    parser = argparse.ArgumentParser(
        __name__, description="import a raster into a geoserver"
    )
    parser.add_argument("-u", "--user", default="admin")
    parser.add_argument("-n", "--workspace_name", default="enermaps")
    parser.add_argument("-r", "--is_raster", default="False")
    parser.add_argument(
        "-b",
        "--base_url",
        default="http://127.0.0.1:8000/geoserver",
        help="base url to reach the geoserver",
    )
    parser.add_argument("geofile")
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    return parser


def main():
    """Main """
    parser = get_parser()
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    import_file(
        base_url=args.base_url,
        user=args.user,
        password=os.environ["GEOSERVER_PASS"],
        file_path=args.shapefile,
        workspace_name=args.workspace_name,
        is_raster=args.is_raster,
    )


if __name__ == "__main__":
    main()
