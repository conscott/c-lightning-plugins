from collections import defaultdict
from lib.amount import Amount

# Default max channel size (for now)
WUMBO = Amount(16777216, 'sat')


# Get own node id
def nodeid(rpc):
    return rpc.getinfo()['id']


# Get total onchain funds including unconfirmed
def onchain_balance(rpc):
    return Amount(sum((int(x["value"])
                       for x in rpc.listfunds()["outputs"])), 'sat')


# Get total unconfirmed onchain funds
def onchain_confirmed_balance(rpc):
    return Amount(sum((int(x["value"])
                       for x in rpc.listfunds()["outputs"]
                       if x["status"] == "confirmed")), 'sat')


# Get total confirmed onchain funds
def onchain_unconfirmed_balance(rpc):
    return Amount(sum((int(x["value"])
                       for x in rpc.listfunds()["outputs"]
                       if x["status"] == "unconfirmed")), 'sat')


# Get total capacity of node by node_id
def get_node_capacity(rpc, node_id):
    return Amount(sum((c['satoshis'] for c in rpc.listchannels()['channels']
                       if c['source'] == node_id)), 'sat')


# Get map of nodeid -> total-capacity
def nodes_by_capacity(rpc):
    channels = rpc.listchannels()['channels']
    capacity = defaultdict(int)
    for c in channels:
        capacity[c['source']] += c['satoshis']
    return capacity


# Get map of nodeid -> num-channels
def nodes_by_channels(rpc):
    channels = rpc.listchannels()['channels']
    channel_count = defaultdict(int)
    for c in channels:
        channel_count[c['source']] += 1
    return channel_count


# Get list of top N capacity nodes, with optional ignore list of node_ids
def top_n_capacity(rpc, n, ignore=[]):
    caps = nodes_by_capacity(rpc)
    return [{'node_id': nid, 'capacity_sat':  caps[nid]}
            for nid in sorted(caps, key=caps.get, reverse=True)
            if nid not in ignore][:n]


# Get list of top N nodes with most channels, with optional ignore list of node_ids
def top_n_channel(rpc, n, ignore=[]):
    chans = nodes_by_channels(rpc)
    return [{'node_id': nid, 'num_channels':  chans[nid]}
            for nid in sorted(chans, key=chans.get, reverse=True)
            if nid not in ignore][:n]
