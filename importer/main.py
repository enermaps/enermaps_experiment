#!/usr/bin/env python3
"""This import a simple raster into the geoserver
"""
import argparse
import logging
import os
from collections import defaultdict

import requests

nested_dict = lambda: defaultdict(nested_dict)
NestedDict = nested_dict()


class GeoserverImportError(Exception):
    pass


class GeoserverImporter:
    DATASTORE = {"dataStore": {"name": "geoserver_db"}}

    def __init__(self, base_url, user, password):
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.base_url = base_url.rstrip("/")

    def getImportCreationPayload(self, workspace_name):
        import_creation_payload = NestedDict
        import_creation_payload["import"]["targetWorkspace"]["workspace"][
            "name"
        ] = workspace_name
        import_creation_payload["targetStore"] = self.DATASTORE
        return import_creation_payload

    def import_file(self, file_path, workspace_name, is_raster=False, projection=None):
        import_creation_payload = self.getImportCreationPayload(workspace_name)
        url = self.base_url + "/rest/imports"
        resp = self.session.post(url, json=import_creation_payload)
        if not resp.ok:
            raise GeoserverImportError(resp.text)
        resp_payload = resp.json()
        import_id = resp_payload["import"]["id"]

        filename = os.path.basename(file_path)
        url = self.base_url + "/rest/imports/{!s}/tasks".format(import_id)
        with open(file_path, "br") as geofile:
            resp = self.session.post(url, files={"name": filename, "filedata": geofile})
            logging.info(resp, resp.text)
            if not resp.ok:
                raise GeoserverImportError(resp.text)

        if not is_raster:
            # the file doesn't have a store set, so it will default to the default store
            # currently we don't support importing raster file to postgis directly
            url = self.base_url + "/rest/imports/{!s}/tasks/0/target".format(import_id)
            resp = self.session.put(url, json=self.DATASTORE)
            if not resp.ok:
                raise GeoserverImportError(resp.text)
            logging.info(resp, resp.text)

        url = self.base_url + "/rest/imports/{!s}".format(import_id)
        resp = self.session.post(url)
        if not resp.ok:
            raise GeoserverImportError(resp.text)
        logging.info(resp, resp.text)


def get_parser():
    """return the cli command parser"""
    parser = argparse.ArgumentParser(
        __name__, description="import a raster into a geoserver"
    )
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
    geoserver_importer = GeoserverImporter(
        user=os.environ["GEOSERVER_USER"],
        password=os.environ["GEOSERVER_PASS"],
        base_url=args.base_url,
    )
    geoserver_importer.import_file(
        file_path=args.geofile,
        workspace_name=args.workspace_name,
        is_raster=args.is_raster,
    )


if __name__ == "__main__":
    main()
