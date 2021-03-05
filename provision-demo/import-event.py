#!/usr/bin/env python3

import sys
sys.path.insert(0, "/var/www/MISP/PyMISP/examples/")
from pymisp import PyMISP, MISPAttribute, MISPEvent, MISPEventBlocklist, ExpandedPyMISP
from keys import misp_url, misp_key, misp_verifycert, misp_client_cert
import json
import argparse
import re
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import events from json file.')
    parser.add_argument("-i", "--input", required=True, help="Input file")
    args = parser.parse_args()

    misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert, debug=False, proxies=False)
    subst = "\"timestamp\": \"{ts}\"".format(ts=int(time.time()))
    regex = r"\"timestamp\": \"[0-9]{10}\""
    subst_publish = "\"publish_timestamp\": \"{ts}\"".format(ts=int(time.time()))
    regex_publish = r"\"publish_timestamp\": \"[0-9]{10}\""
    if args.input:
        with open(args.input, 'r') as f:
            for e in f:
                event = json.loads(e)['response'][0]
                eventid = event["Event"]["id"]
                eventuuid = event["Event"]["uuid"]
                eventinfo = event["Event"]["info"] 

                # Delete event and remove it from the blocklist
                misp.delete_event(eventuuid)
                misp.delete_event_blocklist(eventuuid)

                # Fetch the new event, replace timestamps and push the event
                res = json.dumps(event)
                res = re.sub(regex, subst, res, 0, re.MULTILINE)
                res = re.sub(regex_publish, subst_publish, res, 0, re.MULTILINE)
                res = misp.add_event(res)
                print("----------------------------------------")
                if 'errors' in res:
                    print(res)
                else:
                    print("Processed {eventid} - {eventinfo}".format(eventid=eventid,eventinfo=eventinfo))
                print("----------------------------------------")
