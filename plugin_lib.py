from collections import defaultdict

WUMBO = 16777216

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

msat_convert = {
    'msat': 1.0,
    'sat': 1000.0,
    'mbtc': 10**8.0,
    'btc': 10**11.0
}

sat_convert = {
    'msat': 0.001,
    'sat': 1.0,
    'mbtc': 10**5.0,
    'btc': 10**8.0
}

mbtc_convert = {
    'msat': 0.00000001,
    'sat': 0.00001,
    'mbtc': 1.0,
    'btc': 10**3.0
}

btc_convert = {
    'msat': 0.00000000001,
    'sat': 0.00000001,
    'mbtc': 0.001,
    'btc': 1.0
}

convert = {
    'msat': msat_convert,
    'sat': sat_convert,
    'mbtc': mbtc_convert,
    'btc': btc_convert
}


class Amount():

    def __init__(self, amount, unit):

        if not is_valid_unit(unit):
            raise ValueError("Invalid btc unit %s, must be in %s" % (unit, valid_units))

        self._amt = amount
        self._unit = unit.lower()

        def to(to_unit):
            return (self._amt * convert[self._unit][to_unit])

        def __str__(self):
            return "Amount %s %s " % (self._amt, self._unit)


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


def convert_mbtc(val, unit):
    return val / mbtc_convert[unit.lower()]


def convert_btc(val, unit):
    return val / btc_convert[unit.lower()]


def channel_pending(state):
    return state == 'CHANNELD_AWAITING_LOCKIN'


def channel_active(state):
    return (state != 'FUNDING_SPEND_SEEN' and
            state != 'CLOSINGD_COMPLETE' and
            state != 'ONCHAIN')


def channel_closed(state):
    return not (channel_pending(state) or channel_active(state))


""" ------------------ Calcs for own node ----------------------
"""


# All channels awaiting lockin
def pending_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_pending(p['channels'][0]['state'])]


# All channels in active state
def active_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_active(p['channels'][0]['state'])]


# All recently closed channels
def closed_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_closed(p['channels'][0]['state'])]


# Channels funded by remote peer
def incoming_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] <= 0]


# Channels funded by local node
def outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] > 0]


# Active channels funded remotely
def active_incoming_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_active(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] <= 0]


# Active channels funded locally
def active_outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_active(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] > 0]


# Pending channels funded remotely
def pending_incoming_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_pending(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] <= 0]


# Pending channels funded locally
def pending_outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_pending(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] > 0]


# Closed channels funded remotely
def closed_incoming_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_closed(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] <= 0]


# Closed channels funded locally
def closed_outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_closed(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][get_nodeid(rpc)] > 0]


# List all connected peers with no active channels
def peers_no_channel(rpc):
    return [p for p in rpc.listpeers()['peers']
            if not p['channels']]


# List channels with total capacity greater than given amount
def channels_greater_than(rpc, amount, unit):
    if not is_valid_unit(unit):
        return "Value units are %s" % ', '.join(valid_units)

    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and convert_msat(p['channels'][0]['msatoshi_total'], unit) >= amount]


# List channels with total capacity less than given amount
def channels_less_than(rpc, amount, unit):
    if not is_valid_unit(unit):
        return "Value units are %s" % ', '.join(valid_units)

    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and convert_msat(p['channels'][0]['msatoshi_total'], unit) <= amount]


# Filter channels by some stuff
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


# Sum local balance of all active channels
def active_balance(rpc):
    return Amount(sum((p['channel'][0]['msatoshi_to_us'] for p in active_channels(rpc))), 'msat')


# Sum local balance of all pending channels
def pending_balance(rpc):
    return Amount(sum((p['channel'][0]['msatoshi_to_us'] for p in pending_channels(rpc))), 'msat')


# Sum local balance of all closed channels
def closed_balance(rpc):
    return Amount(sum((p['channel'][0]['msatoshi_to_us'] for p in closed_channels(rpc))), 'msat')


# Sum remote balance of all active channels
def active_incoming_balance(rpc):
    return Amount(sum((p['channel'][0]['msatoshi_total'] - p['channel'][0]['msatoshi_to_us']
                  for p in active_channels(rpc))), 'msat')


# Sum remote balance of all pending channels
def pending_incoming_balance(rpc):
    return Amount(sum((p['channel'][0]['msatoshi_total'] - p['channel'][0]['msatoshi_to_us']
                  for p in pending_channels(rpc))), 'msat')


# Sum remote balance of all closed channels
def closed_incoming_balance(rpc):
    return Amount(sum((p['channel'][0]['msatoshi_total'] - p['channel'][0]['msatoshi_to_us']
                  for p in closed_channels(rpc))), 'msat')


# Total funded locally
def funded_outgoing_balance(rpc):
    return Amount(sum((p['channel'][0]['msatoshi_total'] for p in outgoing_channels(rpc))), 'msat')


# Total funded remotely
def funded_incoming_balance(rpc):
    return Amount(sum((p['channel'][0]['msatoshi_total'] for p in incoming_channels(rpc))), 'msat')


# Total local reserve balance
def reserve_balance(rpc):
    return Amount(sum((p['channel'][0]['our_channel_reserve_satoshis'] for p in active_channels(rpc))), 'msat')


# Total spendable balance is your active balance - reserve balance
def spendable_balance(rpc):
    return Amount(active_balance(rpc) - reserve_balance(rpc), 'msat')


# Total routing fees paid thus far on node
def routing_fees_paid(rpc):
    return Amount(sum((p['msatoshi_sent'] - p['msatoshi']
                       for p in rpc.listpayments()['payments']
                       if p['status'] == 'complete')), 'msat')


# Total received in invoices
def total_paid_invoices(rpc):
    return Amount(sum((i['msatoshi_received'] for i in rpc.listinvoices()['invoices']
                       if i['status'] == 'paid')), 'msat')


# Total in invoices that have not been paid yet
def total_unpaid_invoices(rpc):
    return Amount(sum((i['msatoshi'] for i in rpc.listinvoices()['invoices']
                       if i['status'] == 'unpaid')), 'msat')


# Total in invoices that have expired
def total_expired_invoices(rpc):
    return Amount(sum((i['msatoshi'] for i in rpc.listinvoices()['invoices']
                       if i['status'] == 'expired')), 'msat')


# Get total onchain funds
def onchain_balance(rpc):
    return Amount(sum((int(x["value"]) for x in rpc.listfunds()["outputs"])), 'sat')


""" ------------------ Calcs for other nodes ----------------------
"""


<<<<<<< HEAD
def onchain_confirmed_sat(rpc):
    return sum([int(x["value"]) for x in rpc.listfunds()["outputs"]
                if x["status"] == "confirmed"])


def onchain_pending_sat(rpc):
    return sum([int(x["value"]) for x in rpc.listfunds()["outputs"]
               if x["status"] == "unconfirmed"])


=======
# Get total capacity of node by node_id
>>>>>>> Major additions to plugin lib, wip
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
