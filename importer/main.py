#!/usr/bin/env python3
"""This import a simple raster into the geoserver
"""
import argparse
import collections
import logging
import os
import posixpath
from typing import Text, Iterable, Tuple
from collections import defaultdict

import requests

from importer import GeoserverImporter

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
