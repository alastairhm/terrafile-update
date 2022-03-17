#!/usr/bin/env python3

import os
import json
import urllib3
import argparse
import yaml
from yaml.loader import SafeLoader


def main():
    urllib3.disable_warnings()
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    token = os.environ["GIT_TOKEN"]

    parser = argparse.ArgumentParser(description='Upgrade Terrafile module versions')
    parser.add_argument("-i","--input",type=str,help="Input Terrafile YAML, default=Terrafile", default="Terrafile")
    parser.add_argument("-o","--output",type=str,help="Input Terrafile YAML, default=Terrafile.new", default="Terrafile.new")
    parser.add_argument("-m","--major", action='store_true',help="Update major versions of modules")
    parser.add_argument("-v","--verbose", action='store_true',help="Verbose output")
    args = parser.parse_args()

    if os.path.isfile(args.input):
        terrafile = []
        dirty = False
        with open(args.input, "r") as f:
            terrafile = list(yaml.load_all(f, Loader=SafeLoader))
            terrafile = terrafile[0]

        print('Checking versions...')
        for repo in terrafile:
            if args.verbose:
                print('Repo [',repo,']')
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
            if version not in (tags[0]['name'], 'master', 'main'):
                if args.verbose:
                    print(version,'-->',tags[0]["name"])
                terrafile[repo]["version"] = tags[0]["name"]
                dirty = True
        if dirty:
            print('Writting new file...')
            with open(args.output, "w") as f:
                f.write(yaml.dump(terrafile))
        else:
            print('No changes required')
    else:
        print('Error : Input file not found')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
