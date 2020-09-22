"""Integration test for the importer
"""
import os
import subprocess
import time
import unittest

import geoserver_init
import main
from dotenv import load_dotenv

DOCKER_COMPOSE_PROJECT = "import_integration_test"
DOCKER_COMPOSE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEOSERVER_BASE_URL = "http://127.0.0.1:8000/geoserver"


def docker_compose(*args):
    """run the docker-compose command"""
    command = ["docker-compose"]
    command += ["--project-directory", DOCKER_COMPOSE_DIR]
    command += ["--project-name", DOCKER_COMPOSE_PROJECT]
    command += ["--no-ansi"]
    command += args
    print("running", command)
    subprocess.check_output(command)


class TestImport(unittest.TestCase):
    """Test the import function on a set of files"""

    def test_geotiff_import(self):
        """Test the run of the importer on a geotiff raster file"""
        main.import_file(
            GEOSERVER_BASE_URL,
            user=os.environ["GEOSERVER_USER"],
            password=os.environ["GEOSERVER_PASS"],
            file_path="testdata/hotmaps-cdd_curr.tif",
            workspace_name=os.environ["WORKSPACE"],
            is_raster=False,
        )

    def test_shapefile_import(self):
        """Test the run of the importer on a gml file"""
        main.import_file(
            GEOSERVER_BASE_URL,
            user=os.environ["GEOSERVER_USER"],
            password=os.environ["GEOSERVER_PASS"],
            file_path="testdata/bau_final_energy_consumption_view.gml",
            workspace_name=os.environ["WORKSPACE"],
            is_raster=True,
        )


def setUpModule():
    """"""
    print("loading setup")
    load_dotenv("../.env")
    # verify that the stack is down
    docker_compose("down")
    docker_compose("rm")
    docker_compose("up", "--build", "-d", "geoserver", "db")
    time.sleep(60)
    # init the geoserver
    geoserver_init.init()


def tearDownModule():
    """"""
    docker_compose("down")


if __name__ == "__main__":
    unittest.main()
