#!/usr/bin/env python3
"""This import a simple raster into the geoserver
"""
import argparse
import logging
import os
from collections import defaultdict

import requests

NestedDict = lambda: defaultdict(nested_dict)
nest = NestedDict()


class ImportError(Exception):
    pass


def get_import_creation_payload(workspace_name):
    import_creation_payload = NestedDict()
    import_creation_payload["import"]["targetWorkspace"]["workspace"][
        "name"
    ] = workspace_name
    return import_creation_payload


def import_file(base_url, user, password, file_path, workspace_name):

    session = requests.Session()
    session.auth = (user, password)
    import_creation_payload = get_import_creation_payload(workspace_name)
    resp = session.post(url, json=import_creation_payload)
    if not resp.ok:
        raise ImportError(resp.text)
    resp_payload = resp.json()
    import_id = resp_payload["import"]["id"]

    filename = os.path.basename(file_path)
    url = "http://localhost:8000/geoserver/rest/imports/{!s}/tasks".format(import_id)
    with open(file_path, "br") as shapefile:
        resp = session.post(url, files={"name": filename, "filedata": shapefile})
        logging.info(resp, resp.text)
        if not resp.ok:
            raise ImportError(resp.text)
    resp = session.post(
        "http://localhost:8000/geoserver/rest/imports/{!s}".format(import_id)
    )
    logging.info(resp, resp.text)


def get_parser():
    """return the cli command parser"""
    parser = argparse.ArgumentParser(
        __name__, description="import a raster into a geoserver"
    )
    parser.add_argument("-u", "--user", default="admin")
    parser.add_argument(
        "-b",
        "--base_url",
        default="http://127.0.0.1:8000/geoserver",
        help="base url to reach the geoserver",
    )
    parser.add_argument("shapefile")
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
    )


if __name__ == "__main__":
    main()
