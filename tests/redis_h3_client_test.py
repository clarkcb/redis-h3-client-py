#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# redis_h3_client_test.py
#
# Test the RedisH3 client class
#
################################################################################
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis_h3_client import RedisH3


class RedisH3Test(unittest.TestCase):
    h3_set_key = 'H3TestKey'
    test_data = {
        'entries': [
            {
                'name': 'Catania',
                'lng': '15.087269',
                'lat': '37.502669',
                'h3key': '8f3f35c64acb125',
                'h3idx': '645126749795692837',
                'parentkey': '833f35fffffffff'
            },
            {
                'name': 'Palermo',
                'lng': '13.361389',
                'lat': '38.115556',
                'h3key': '8f1e9a0ec840645',
                'h3idx': '644553099062806085',
                'parentkey': '831e9afffffffff'
            }
        ]
    }

    def get_redis_h3_client(self):
        return RedisH3(host='localhost', port=6379, db=0)

    def get_redis_h3_client_and_setup(self):
        """Get client and set db to default state"""
        client = self.get_redis_h3_client()
        if client.exists(self.h3_set_key):
            client.delete(self.h3_set_key)
        return client

    # since we need to add entries for most tests, do this in separate method
    def add_entries(self, client):
        values = []
        for e in self.test_data['entries']:
            values.extend([e['lng'], e['lat'], e['name']])
        res = client.h3_add(self.h3_set_key, *values)
        return res

    def add_entries_by_index(self, client):
        values = []
        for e in self.test_data['entries']:
            values.extend([e['h3key'], e['name'] + '-key'])
            values.extend([e['h3idx'], e['name'] + '-idx'])
        res = client.h3_addbyindex(self.h3_set_key, *values)
        return res

    def test_h3_status(self):
        client = self.get_redis_h3_client()
        res = client.h3_status()
        self.assertEqual(b'Ok', res)

    def test_h3_add(self):
        client = self.get_redis_h3_client_and_setup()
        res = self.add_entries(client)
        expected_res = len(self.test_data['entries'])
        self.assertEqual(expected_res, res)
        self.assertEqual(expected_res, client.zcard(self.h3_set_key))

    def test_h3_addbyindex(self):
        client = self.get_redis_h3_client_and_setup()
        res = self.add_entries(client)
        expected_res = len(self.test_data['entries']) * 2
        res = self.add_entries_by_index(client)
        self.assertEqual(expected_res, res)
        expected_card = len(self.test_data['entries']) * 3
        self.assertEqual(expected_card, client.zcard(self.h3_set_key))

    def test_h3_scan(self):
        client = self.get_redis_h3_client_and_setup()
        res = self.add_entries(client)

        # 1) scan all
        expected_res_len = len(self.test_data['entries'])
        res = client.h3_scan(self.h3_set_key, 0)
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res_len, len(res[1]))

        # 2) scan with match pattern
        start_letter = 'P'
        match_pattern = '{start_letter}*'.format(start_letter=start_letter)
        expected_res_len = len([e['name'] for e in self.test_data['entries'] if e['name'].startswith(start_letter)])
        res = client.h3_scan(self.h3_set_key, 0, match=match_pattern)
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res_len, len(res[1]))

    def test_h3_index(self):
        client = self.get_redis_h3_client_and_setup()
        res = self.add_entries(client)
        entry_names = [e['name'] for e in self.test_data['entries']]
        expected_res_len = len(self.test_data['entries'])
        res = client.h3_index(self.h3_set_key, *entry_names)
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res_len, len(res))

    def test_h3_pos(self):
        client = self.get_redis_h3_client_and_setup()
        res = self.add_entries(client)
        entry_names = [e['name'] for e in self.test_data['entries']]
        expected_res_len = len(self.test_data['entries'])
        res = client.h3_pos(self.h3_set_key, *entry_names)
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res_len, len(res))

    def test_h3_count(self):
        client = self.get_redis_h3_client_and_setup()
        # add entries by lng/lat and also index (key and long forms) so there are 3 entries per h3idx
        res = self.add_entries(client)
        res = self.add_entries_by_index(client)
        for entry in self.test_data['entries']:
            expected_res = 3
            res = client.h3_count(self.h3_set_key, entry['parentkey'])
            print('res: {res}'.format(res=res))
        self.assertEqual(expected_res, res)

    def test_h3_cell(self):
        client = self.get_redis_h3_client_and_setup()
        # add entries by lng/lat and also index (key and long forms) so there are 3 entries per h3idx
        res = self.add_entries(client)
        res = self.add_entries_by_index(client)

        for entry in self.test_data['entries']:
            # 1) get all
            expected_res_len = 3
            res = client.h3_cell(self.h3_set_key, entry['parentkey'])
            print('res: {res}'.format(res=res))
            self.assertEqual(expected_res_len, len(res))

            # 2) get all with indices
            expected_res_len = 6
            res = client.h3_cell(self.h3_set_key, entry['parentkey'], withindices=True)
            print('res: {res}'.format(res=res))
            self.assertEqual(expected_res_len, len(res))

            # 3) get with limit offset/count
            expected_res_len = 1
            res = client.h3_cell(self.h3_set_key, entry['parentkey'], offset=1, count=1)
            print('res: {res}'.format(res=res))
            self.assertEqual(expected_res_len, len(res))

    def test_h3_dist(self):
        client = self.get_redis_h3_client_and_setup()
        res = self.add_entries(client)

        # 1) get distance in default unit (meters)
        expected_res = b'166274.6888'
        entry_names = [e['name'] for e in self.test_data['entries']]
        res = client.h3_dist(self.h3_set_key, *entry_names)
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res, res)

        # 2) get distance in km
        expected_res = b'166.2747'
        values = entry_names + ['km']
        res = client.h3_dist(self.h3_set_key, *values)
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res, res)

        # 3) get distance in ft
        expected_res = b'545520.6324'
        values = entry_names + ['ft']
        res = client.h3_dist(self.h3_set_key, *values)
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res, res)

        # 4) get distance in mi
        expected_res = b'103.3186'
        values = entry_names + ['mi']
        res = client.h3_dist(self.h3_set_key, *values)
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res, res)

    def test_h3_rembyindex(self):
        client = self.get_redis_h3_client_and_setup()
        res = self.add_entries(client)
        expected_res = 1
        res = client.h3_rembyindex(self.h3_set_key, self.test_data['entries'][0]['h3key'])
        print('res: {res}'.format(res=res))
        self.assertEqual(expected_res, res)
        expected_card = len(self.test_data['entries']) - 1
        self.assertEqual(expected_card, client.zcard(self.h3_set_key))
