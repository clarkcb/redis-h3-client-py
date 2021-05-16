#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# redis_h3_client.py
#
# A redis client that includes methods for H3 module commands
#
################################################################################

import redis
from redis.exceptions import (
    DataError,
)


class RedisH3(redis.Redis):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug = False

    def h3_add(self, name: str, *values):
        """
        H3.ADD [key] [lng1] [lat1] [name1] [lng2] [lat2] [name2] ...
        """
        if len(values) % 3 != 0:
            raise DataError("H3.ADD requires places with lon, lat and name"
                            " values")
        h3add_command = ['H3.ADD', name, *values]
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3add_command])))
        return self.execute_command(*h3add_command)

    def h3_addbyindex(self, name: str, *values):
        """
        H3.ADDBYINDEX [key] [h3idx1] [name1] [h3idx2] [name2] ...
        """
        if len(values) % 2 != 0:
            raise DataError("H3.ADDBYINDEX requires places with h3idx and name"
                            " values")
        h3addbyindex_command = ['H3.ADDBYINDEX', name, *values]
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3addbyindex_command])))
        return self.execute_command(*h3addbyindex_command)

    def h3_cell(self, name: str, h3_index, withindices=False, offset=0, count=0):
        """
        H3.CELL [key] [h3idx] [WITHINDICES] [LIMIT offset count]
        """
        h3cell_command = ['H3.CELL', name, h3_index]
        if withindices:
            h3cell_command.append('WITHINDICES')
        if offset or count:
            h3cell_command.extend(['LIMIT', offset, count])
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3cell_command])))
        return self.execute_command(*h3cell_command)

    def h3_count(self, name: str, h3_index):
        """
        H3.COUNT [key] [h3idx]
        """
        h3count_command = ['H3.COUNT', name, h3_index]
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3count_command])))
        return self.execute_command(*h3count_command)

    def h3_dist(self, name: str, elem1: str, elem2: str, unit: str = 'm'):
        """
        H3.DIST [key] [elem1] [elem2] [m|km|ft|mi]
        """
        h3dist_command = ['H3.DIST', name, elem1, elem2, unit]
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3dist_command])))
        return self.execute_command(*h3dist_command)

    def h3_index(self, name: str, *values):
        """
        H3.INDEX [key] [elem1] [elem2] ...
        """
        h3index_command = ['H3.INDEX', name, *values]
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3index_command])))
        return self.execute_command(*h3index_command)

    def h3_pos(self, name: str, *values):
        """
        H3.POS key [elem1] [elem2] ...
        """
        h3pos_command = ['H3.POS', name, *values]
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3pos_command])))
        pos_as_bytes = self.execute_command(*h3pos_command)
        return [(float(p[0]), float(p[1])) for p in pos_as_bytes]

    def h3_rembyindex(self, key: str, *values):
        """
        H3.REMBYINDEX key [elem1] [elem2] ...
        """
        h3rembyindex_command = ['H3.REMBYINDEX', key, *values]
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3rembyindex_command])))
        res = self.execute_command(*h3rembyindex_command)
        return res

    def h3_scan(self, key: str, cursor: int = 0, match: str = None, count: int = 0):
        """
        H3.SCAN key cursor [MATCH pattern] [COUNT count]
        """
        h3scan_command = ['H3.SCAN', key, cursor]
        if match is not None:
            h3scan_command.extend(['MATCH', match])
        if count:
            h3scan_command.extend(['COUNT', count])
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3scan_command])))
        (next_cursor, res) = self.execute_command(*h3scan_command)
        pairs = [(res[i], res[i+1]) for i in range(0, len(res), 2)]
        return (int(next_cursor), pairs)

    def h3_status(self):
        """
        H3.STATUS
        """
        h3status_command = ['H3.STATUS']
        if self.debug:
            print('{}'.format(' '.join([str(c) for c in h3status_command])))
        res = self.execute_command(*h3status_command)
        return res
