#!/usr/bin/env python3

import yaml
import os
import urllib3
import json
from yaml.loader import SafeLoader

urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE')
token = os.environ["GIT_TOKEN"]

terrafile = []
with open("Terrafile", "r") as f:
    terrafile = list(yaml.load_all(f, Loader=SafeLoader))
    terrafile = terrafile[0]

for repo in terrafile:
    print(repo)
    details = terrafile[repo]
    source = details["source"].split('/')
    tail = source[3]
    for elem in source[4:]:
        tail = tail + '%2F' + elem
    api = 'https://'+source[2]+'/api/v4/projects/'+tail+'/repository/tags'
    version = details["version"]
    r = http.request(
        'GET',
        api,
        headers={
            'PRIVATE-TOKEN': token
        }
    )

    tags = json.loads(r.data.decode('utf-8'))
    if (version != tags[0]["name"] and version != 'master' and version != 'main'):
        print(version,tags[0]["name"])
        terrafile[repo]["version"] = tags[0]["name"]
with open("Terrafile.new", "w") as f:
    f.write(yaml.dump(terrafile))
