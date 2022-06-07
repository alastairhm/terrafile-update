#!/usr/bin/env python3
"""Update Terrafile to latest versions."""

import os
import sys
import json
import argparse
import urllib3
import yaml
from yaml.loader import SafeLoader

def major_update(current, new):
    """Check if major version bump."""
    status = current.split('.')[0] != new.split('.')[0]
    return status

def generate_url(details):
    """Format URL for API call"""
    source = details["source"].split('/')
    tail = source[3]
    for elem in source[4:]:
        tail = tail + '%2F' + elem
    api = 'https://'+source[2]+'/api/v4/projects/'+tail+'/repository/tags'
    return api


def main():
    """Update Terrafile to latest versions."""

    urllib3.disable_warnings()
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    token = os.environ["GIT_TOKEN"]

    parser = argparse.ArgumentParser(description='Upgrade Terrafile module versions')
    parser.add_argument("-i","--input",type=str,help="Input Terrafile YAML, default=Terrafile",
                        default="Terrafile")
    parser.add_argument("-o","--output",type=str,help="Input Terrafile YAML, default=Terrafile.new",
                        default="Terrafile.new")
    parser.add_argument("-m","--major", action='store_true',help="Update major versions of modules")
    parser.add_argument("-v","--verbose", action='store_true',help="Verbose output")
    parser.add_argument("-c","--check", action='store_true',help="Just check no output")
    args = parser.parse_args()
    if args.verbose:
        print("Arguements :",args)

    if os.path.isfile(args.input):
        terrafile = []
        dirty = False
        major_changes = False
        with open(args.input, "r") as input_file:
            terrafile = list(yaml.load_all(input_file, Loader=SafeLoader))
            terrafile = terrafile[0]

        print('Checking versions...')
        for repo in terrafile:
            if args.verbose:
                print('Repo [',repo,']')
            details = terrafile[repo]
            version = details["version"]
            api = generate_url(details)
            response = http.request(
                'GET',
                api,
                headers={
                    'PRIVATE-TOKEN': token
                }
            )

            tags = json.loads(response.data.decode('utf-8'))
            if tags != [] and version not in (tags[0]['name'], 'master', 'main'):
                major_bump = major_update(version,tags[0]["name"])
                if not major_bump or args.major:
                    if args.verbose:
                        print(version,'-->',tags[0]["name"])
                    terrafile[repo]["version"] = tags[0]["name"]
                    dirty = True
                else:
                    major_changes = True
        if major_changes and not args.major:
            print('Warning : Major version changes detected and not actioned.')
        if dirty:
            if not args.check:
                print('Writing new file...')
                with open(args.output, "w") as output_file:
                    output_file.write(yaml.dump(terrafile))
            else:
                print("Updates detected.")
                return 1
        else:
            print('No changes required.')
    else:
        print('Error : Input file not found')
        return 1
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(e)
        sys.exit(1)
