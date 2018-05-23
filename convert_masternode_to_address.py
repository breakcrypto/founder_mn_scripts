#Use this script to convert a collection of masternode tx ids
#to wallet addresses

import time
import urllib2
import json

masternode_addresses = []

url_base = "http://explorer.foxrtb.com/api/tx/"

with open('masternodes.txt') as f:
    masternodes = f.read().splitlines()

for masternode_tx in masternodes:

    req = urllib2.Request(url_base + masternode_tx)
    opener = urllib2.build_opener()
    f = opener.open(req)
    parsed = json.loads(f.read())

    # check the outbound transactions

    for vout in parsed['vout']:
        spentTx = vout['spentTxId']

        if spentTx is None and float(vout['value']) == 500000.0:
            address = vout['scriptPubKey']['addresses'][0]
            masternode_addresses.append(address)
            print address

    time.sleep(1)

print ' '
print ' '
print '------------------------------------'
print '------------------------------------'
print '------------------------------------'
print ' '
print ' '

set_mn = set(masternode_addresses)
for mn in set_mn:
    print mn