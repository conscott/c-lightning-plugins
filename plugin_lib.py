from collections import defaultdict

NO_WUMBO = 16777216

valid_units = (
    'msat',
    'sat',
    'mbtc',
    'btc'
)

channel_filters = (
   'pending',
   'active',
   'closed',
   'incoming',
   'outgoing',
   'greater_than',
   'less_than'
)

sat_convert = {
    'msat': 0.001,
    'sat': 1.0,
    'mbtc': 10**5.0,
    'btc': 10**8.0
}

msat_convert = {
    'msat': 1.0,
    'sat': 1000.0,
    'mbtc': 10**8.0,
    'btc': 10**11.0
}


def get_nodeid(rpc):
    return rpc.getinfo()['id']


def is_valid_unit(unit):
    return unit.lower() in valid_units


def is_valid_filter(f):
    return f.lower() in channel_filters


def convert_msat(val, unit):
    return val / msat_convert[unit.lower()]


def convert_sat(val, unit):
    return val / sat_convert[unit.lower()]


def channel_pending(state):
    return state == 'CHANNELD_AWAITING_LOCKIN'


def channel_active(state):
    return (state != 'FUNDING_SPEND_SEEN' and
            state != 'CLOSINGD_COMPLETE' and
            state != 'ONCHAIN')


def channel_closed(state):
    return not (channel_pending(state) or channel_active(state))


def pending_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and channel_pending(p['channels'][0]['state'])]


def active_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and channel_active(p['channels'][0]['state'])]


def closed_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and channel_closed(p['channels'][0]['state'])]


def incoming_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] <= 0]


def outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] > 0]


def channels_greater_than(rpc, amount, unit):
    if not is_valid_unit(unit):
        return "Value units are %s" % ', '.join(valid_units)

    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and convert_msat(p['channels'][0]['msatoshi_total'], unit) >= amount]


def channels_less_than(rpc, amount, unit):
    if not is_valid_unit(unit):
        return "Value units are %s" % ', '.join(valid_units)

    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and convert_msat(p['channels'][0]['msatoshi_total'], unit) <= amount]


def filter_channels(rpc, filter_name, amount=0, unit='msat'):
    if not is_valid_filter(filter_name):
        return "Value filter_name's are %s" % ', '.join(channel_filters)

    if filter_name.lower() == 'pending':
        return pending_channels(rpc)
    if filter_name.lower() == 'active':
        return active_channels(rpc)
    if filter_name.lower() == 'closed':
        return closed_channels(rpc)
    if filter_name.lower() == 'incoming':
        return incoming_channels(rpc)
    if filter_name.lower() == 'outgoing':
        return outgoing_channels(rpc)
    if filter_name.lower() == 'greater_than':
        return channels_greater_than(rpc, amount, unit)
    if filter_name.lower() == 'less_than':
        return channels_less_than(rpc, amount, unit)


# Get total onchain funds
def onchain_sat(rpc):
    return sum([int(x["value"]) for x in rpc.listfunds()["outputs"]])


def get_node_capacity(rpc, node_id):
    sum((c['satoshis'] for c in rpc.listchannels()['channels'] if c['source'] == node_id))


def nodes_by_capacity(rpc):
    channels = rpc.listchannels()['channels']
    capacity = defaultdict(int)
    for c in channels:
        capacity[c['source']] += c['satoshis']
    return capacity


def nodes_by_channels(rpc):
    channels = rpc.listchannels()['channels']
    channel_count = defaultdict(int)
    for c in channels:
        channel_count[c['source']] += 1
    return channel_count


def top_n_capacity(rpc, n, ignore=[]):
    caps = nodes_by_capacity(rpc)
    return [{'node_id': nid, 'capacity_sat':  caps[nid]}
            for nid in sorted(caps, key=caps.get, reverse=True)
            if nid not in ignore][:n]


def top_n_channel(rpc, n, ignore=[]):
    chans = nodes_by_channels(rpc)
    return [{'node_id': nid, 'num_channels':  chans[nid]}
            for nid in sorted(chans, key=chans.get, reverse=True)
            if nid not in ignore][:n]
