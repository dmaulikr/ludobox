#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import shutil

import io
from StringIO import StringIO

from ludobox.webserver import app
from ludobox.config import read_config
from ludobox.content import read_game_info

class TestLudoboxWebServer(unittest.TestCase):

    def setUp(self):

        self.config = read_config()

        # change data dir
        if os.path.exists('/tmp/data'):
            shutil.rmtree('/tmp/data')
        os.makedirs('/tmp/data')

        app.config["DATA_DIR"] = '/tmp/data'

        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):
        result = self.app.get('/')

        # assert the status code of the response (redirected)
        self.assertEqual(result.status_code, 302)

    def test_handshake_page(self):
        result = self.app.get('/api')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data), {"name" : self.config["ludobox_name"]})

    def test_add_game(self):

        valid_info = read_game_info(os.path.join(os.getcwd(), 'tests/test-data/test-game'))

        data = {
            'files': [
                (StringIO('my readme'), 'test-README.txt'),
                (StringIO('my rules'), 'test-RULES.txt'),
                (io.BytesIO(b"abcdef"), 'test.jpg')
            ],
            'info': json.dumps(valid_info)
        }

        result = self.app.post('/api/create',
                                data=data,
                                content_type='multipart/form-data'
                                )

        self.assertEqual(result.status_code, 201)
        res = json.loads(result.data)
        self.assertIn("path", res.keys())

        print res["path"]

        # load JSON info data
        with open(os.path.join(res["path"], 'info.json'), 'r' )as  f:
            stored_info = json.load(f)
        self.assertEqual(stored_info, valid_info)

        # check for files
        written_filenames = os.listdir(os.path.join(res["path"], 'files'))
        self.assertEqual(written_filenames, [f[1] for f in data["files"]])
