"""Integration test for the api server
"""
import logging
import os
import subprocess
import time
import unittest
import posixpath
import urllib.parse

import requests
from dotenv import load_dotenv

DOCKER_COMPOSE_PROJECT = "api_integration_test"
DOCKER_COMPOSE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_BASE_URL = "http://127.0.0.1:9000/api"
API_MAX_RETRY = 10
API_WAIT_SEC = 4


def wait_for_api():
    """wait for the api server
    """
    print("Waiting for the api server")
    for _ in range(API_MAX_RETRY):
        try:
            requests.get(API_BASE_URL)
        except requests.exceptions.ConnectionError:
            print(".", end="", flush=True)
            time.sleep(API_WAIT_SEC)
        else:
            return
    raise Exception(
        "Couldn't reach the api server in {!s} seconds".format(
            API_MAX_RETRY * API_WAIT_SEC
        )
    )

def docker_compose(*args):
    """run the docker-compose command"""
    command = ["docker-compose"]
    command += ["--project-directory", DOCKER_COMPOSE_DIR]
    command += ["--project-name", DOCKER_COMPOSE_PROJECT]
    command += ["--no-ansi"]
    command += args
    logging.info("running: " + str(command))
    subprocess.check_output(command)

class AuthenticationTest(unittest.TestCase):
    USER_ENDPOINT = API_BASE_URL + "/users"
    LOGIN_ENDPOINT = USER_ENDPOINT + "/login"

    def testAuthWithBadPasswordFails(self):
        resp = requests.post(AuthenticationTest.LOGIN_ENDPOINT, json={"email": "rootiiii", "password": "test"})
        self.assertEqual(resp.status_code, 537, resp.text)

    def testAuthWithGoodPasswordSucceed(self):
        print(AuthenticationTest.USER_ENDPOINT)
        resp = requests.post(AuthenticationTest.USER_ENDPOINT, json={"email": "root", "password": "test"})
        self.assertEqual(resp.status_code, 537, resp.text)

class UploadTest(unittest.TestCase):
    UPLOAD_ENDPOINT = API_BASE_URL + "/upload/add"

    def testUploadNotAuthenticatedShouldFail(self):
        #print(UPLOAD_ENDPOINT)
        resp = requests.post(UploadTest.UPLOAD_ENDPOINT)
        self.assertFalse(resp.ok, resp.text)

def setUpModule():
    """"""
    return
    print("loading setup")
    load_dotenv("../.env")
    # verify that the stack is down
    docker_compose("down")
    docker_compose("rm")
    docker_compose("up", "--build", "-d", "api", "db")
    wait_for_api()

def tearDownModule():
    """"""
    return
    docker_compose("down")

if __name__ == "__main__":
     unittest.main()
