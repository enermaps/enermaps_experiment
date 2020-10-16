#!/usr/bin/env python3
import os

import requests

WORKSPACE_TO_DELETE = ("it.geosolutions", "topp", )
def init():
    """From an empty geoserver:
    * Add the enermap workspace if not defined yet.
    * Add the connection to the postgis db if not defined yet
    """
    session = requests.Session()
    session.auth = (os.environ["GEOSERVER_USER"], os.environ["GEOSERVER_PASS"])
    workspace = os.environ["WORKSPACE"]
    url = "http://127.0.0.1:8000/geoserver/rest/workspaces"
    resp = session.post(url, json={"workspace": {"name": workspace, "default": True}})
    for workspace_to_delete in WORKSPACE_TO_DELETE:
        resp = session.delete(url + "/" + workspace_to_delete + "/" + ".DUMMY")
        print(resp, resp.text)
    print(resp, resp.text)

    data_source = {
        "dataStore": {
            "name": "geoserver_db",
            "connectionParameters": {
                "entry": [
                    {"@key": "host", "$": os.environ["GEOSERVER_DB_HOST"]},
                    {"@key": "port", "$": "5432"},
                    {"@key": "database", "$": os.environ["GEOSERVER_DB"]},
                    {"@key": "user", "$": os.environ["GEOSERVER_DB_USER"]},
                    {"@key": "passwd", "$": os.environ["GEOSERVER_DB_PASS"]},
                    {"@key": "dbtype", "$": "postgis"},
                ]
            },
        }
    }
    resp = session.post(
        "http://localhost:8000/geoserver/rest/workspaces/{}/datastores".format(
            workspace
        ),
        json=data_source,
    )
    print(resp, resp.text)


if __name__ == "__main__":
    init()
