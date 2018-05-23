# A sample script demonstrating how you can spider a series of tx
# to identify transactions of interest. In this case any masternodes
# formed from a block of 160,000,000,000 $PAC.

import time
import urllib2
import json

url_base = "http://explorer.foxrtb.com/api/tx/"

#base transaction to start with
transactions = ["e94127b57a79a4b79e7ba7b90d90fc936129a3b30c036890b3a5961d7247a2bb"]

#spider the transactions looking for MNs
for tx in transactions:

    # limit to the 160M block -- this excludes the change from the 160M TX
    if tx == "50c2b34ad8243115f36175e4ff55254c87ee87ad26d6db6463313fda61bff37b":
        continue

    # load information off insight

    req = urllib2.Request(url_base + tx)
    opener = urllib2.build_opener()
    f = opener.open(req)
    parsed = json.loads(f.read())

    # check the outbound transactions

    for vout in parsed['vout']:
        spentHeight = vout['spentHeight']
        spentTx = vout['spentTxId']
        spentIndex = vout['spentIndex']

        # this output has been spent, see where it
        if spentTx is not None:

            if not spentTx in transactions:
                # limit change noise
                if float(vout['value']) > 1.00000000:
                    transactions.append(spentTx)

        else:

            # unspent tx, see if if it's an MN
            if float(vout['value']) == 500000.00000000:
                print tx

    time.sleep(1)