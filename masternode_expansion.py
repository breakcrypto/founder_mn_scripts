# This script can be used to expand a source list of masternodes
# with correlated masternodes. There will likely be some false
# positives

import time
import urllib2
import json

vin_addresses = set()
vout_addresses = set()
private_pac_tx = set()
visited_addresses = set()

url_base = "http://explorer.foxrtb.com/api/addrs/%s/txs"

with open('masternodes.txt') as f:
    masternodes = f.read().splitlines()

for masternode_address in masternodes:

    masternodes.remove(masternode_address)

    if masternode_address in visited_addresses:
        continue

    try:
        req = urllib2.Request(url_base % masternode_address)
        opener = urllib2.build_opener()
        f = opener.open(req)
        parsed = json.loads(f.read())
    except:
        masternodes.append(masternode_address)

    # check the outbound transactions

    for item in parsed['items']:

        if not len(item['vin']) > 3:
            continue

        #loop through and get the addresses

        private_pac = False

        try:
            for vin in item['vin']:

                #record private pac
                if float(vin['value']) == 10.0001 or float(vin['value']) == 100.001 or float(
                        vin['value']) == 1000.01 or float(vin['value']) == 10000.1:
                    private_pac = True
                    private_pac_tx.add(vin['txid'])
                    print "--- PRIVATE PAC ---"
                    break

                #print vin['addr']
                vin_addresses.add(vin['addr'])
        except:
            print 'error processing vin'
            print item

        # uncomment this to enable expansion for vout and privatepac tx'es

        # if private_pac == False:
        #     for vout in item['vout']:
        #         if float(vout['value']) == 10.0001 or float(vout['value']) == 100.001 or float(
        #                 vout['value']) == 1000.01 or float(vout['value']) == 10000.1:
        #             private_pac = True
        #             private_pac_tx.add(vin['txid'])
        #             print "--- PRIVATE PAC ---"
        #             break
        #
        # try:
        #     if private_pac == False:
        #         for vout in item['vout']:
        #             for address in vout['scriptPubKey']['addresses']:
        #
        #                 #print address
        #                 vout_addresses.add(address)
        #
        #                 if address not in masternodes and address not in visited_addresses:
        #                     masternodes.append(address)
        # except:
        #     print 'error processing vout'
        #     print item

    visited_addresses.add(masternode_address)

    time.sleep(2) # be kind to the server

    print 'Remaining Addresses to Check'
    print len(masternodes)

with open("vin_vout.txt", "w") as text_file:
    for mn in vin_addresses:
        text_file.write("%s\n" % mn)

    for mn in vout_addresses:
        text_file.write("%s\n" % mn)

with open("private_pac.txt", "w") as text_file:
    for mn in private_pac_tx:
        text_file.write("%s\n" % mn)