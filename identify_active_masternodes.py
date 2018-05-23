# This script searches the output from masternodelist all
# to a collection of values.

voted_masternodes = []

with open('vin_vout.txt') as f:
    masternodes = f.read().splitlines()

with open('masternode_list_2018_05_22.txt') as f:
    content = f.readlines()

votes = [x.strip() for x in content]

for vote in votes:
    for masternode in masternodes:
        if masternode in vote:
            voted_masternodes.append(vote.split("-")[0][1:])

print ' '
print ' '
print '---------'
print ' '
print ' '

set_mn = set(voted_masternodes)
for mn in set_mn:
    print mn

print len(set_mn)