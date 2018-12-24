#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as rq
import json

# set sonicAPI URL
sonic_url = "https://api.sonicapi.com/"

# set description
access_id = "9290e67a-e9b3-402d-bf84-f5e7898b38f"
input_file = ''

# set param
param = {
    'access_id' = access_id,
                  'input_file' = input_file
}

r_post = rq.post(param)
