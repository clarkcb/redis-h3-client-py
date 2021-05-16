# redis-h3-client-py

#### a python client to a redis server with H3 module loaded

## Overview

The `redis-h3-client-py` repo is a python client of redis server that has the
[redis-h3](https://github.com/clarkcb/redis-h3) module loaded. It depends on the excellent
[redis-py](https://github.com/andymccurdy/redis-py) repo for all non-H3 redis
client functionality.

## Installation

The following requirements are necessary to install and use `redis-h3-client-py`:

* Python 3.x
* a running instance of redis server with [redis-h3](https://github.com/clarkcb/redis-h3) module loaded
* git clone of [redis-h3-client-py](https://github.com/clarkcb/redis-h3-client-py)

You will likely want to install `redis-h3-client-py` as a dependency of another python project.
As of this writing, it has not been published to PyPI, so you will need to install it from the
locally cloned package. Assuming it has been cloned to `$REDIS_H3_CLIENT_PATH`, you would install
like this:

```sh
$ pip3.9 install $REDIS_H3_CLIENT_PATH
```

## Usage

The following table provides the list of client methods currently defined and their corresponding redis-cli command:

| `RedisH3` Method | Redis CLI Command |
| :--------------- | :---------------- |
| `h3_add(name: str, *values)` | `H3.ADD key lng1 lat1 elem1 ... [lngN latN elemN]` |
| `h3_addbyindex(name: str, *values)` | `H3.ADDBYINDEX key h3idx1 elem1 ... [h3idxN elemN]` |
| `h3_cell(name: str, h3_index, withindices=False, offset=0, count=0)` | `H3.CELL key h3idx [WITHINDICES] [LIMIT offset count]` |
| `h3_count(name: str, h3_index)` | `H3.COUNT key h3idx` |
| `h3_dist(name: str, elem1: str, elem2: str, unit: str='m')` | `H3.DIST key elem1 elem2 [m\|km\|ft\|mi]` |
| `h3_index(name: str, *values)` | `H3.INDEX key elem1 ... [elemN]` |
| `h3_pos(name: str, *values)` | `H3.POS key elem1 ... [elemN]` |
| `h3_rembyindex(key: str, *values)` | `H3.REMBYINDEX key h3idx1 ... [h3idxN]` |
| `h3_scan(key: str, cursor: int=0, match: str=None, count: int=0)` | `H3.SCAN key cursor [MATCH pattern] [COUNT count]` |
| `h3_status()` | `H3.STATUS` |

Below is a simple client usage example:

```py
from redis_h3_client import RedisH3

client = RedisH3(host='localhost', port=6379, db=0)

data = {
    'key': 'H3Sicily',
    'entries': [
        {
            'name': 'Catania',
            'lng': '15.087269',
            'lat': '37.502669'
        },
        {
            'name': 'Palermno',
            'lng': '13.361389',
            'lat': '38.115556'
        }
    ]
}

values = []
for e in data['entries']:
    values.extend([e['lng'], e['lat'], e['name']])
res = client.h3_add(data['key'], *values)

# . . .
```

For more usage examples, have a look at the tests in _tests/redis_h3_client_test.py_.
