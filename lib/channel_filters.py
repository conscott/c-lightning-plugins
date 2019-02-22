from amounts import Amount
from node_stats import nodeid

channel_filters = (
   'pending',
   'active',
   'closed',
   'incoming',
   'outgoing',
   'nochannel',
   'greater_than',
   'less_than'
)


# Is a valid channel filter param
def is_valid_filter(f):
    return f.lower() in channel_filters


# Is channel in pending state
def channel_pending(state):
    return state == 'CHANNELD_AWAITING_LOCKIN'


# Is channel in active state
def channel_active(state):
    return (state != 'FUNDING_SPEND_SEEN' and
            state != 'CLOSINGD_COMPLETE' and
            state != 'ONCHAIN')


# Is channel closed
def channel_closed(state):
    return not (channel_pending(state) or channel_active(state))


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
            p['channels'][0]['funding_allocation_msat'][nodeid(rpc)] <= 0]


# Channels funded by local node
def outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            p['channels'][0]['funding_allocation_msat'][nodeid(rpc)] > 0]


# Active channels funded remotely
def active_incoming_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_active(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][nodeid(rpc)] <= 0]


# Active channels funded locally
def active_outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_active(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][nodeid(rpc)] > 0]


# Pending channels funded remotely
def pending_incoming_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_pending(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][nodeid(rpc)] <= 0]


# Pending channels funded locally
def pending_outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_pending(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][nodeid(rpc)] > 0]


# Closed channels funded remotely
def closed_incoming_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_closed(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][nodeid(rpc)] <= 0]


# Closed channels funded locally
def closed_outgoing_channels(rpc):
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            channel_closed(p['channels'][0]['state']) and
            p['channels'][0]['funding_allocation_msat'][nodeid(rpc)] > 0]


# List channels with total capacity greater than given amount
def channels_greater_than(rpc, amount):
    assert type(amount) is Amount
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            Amount(p['channels'][0]['msatoshi_total'], 'msat') >= amount]


# List channels with total capacity less than given amount
def channels_less_than(rpc, amount):
    assert type(amount) is Amount
    return [p for p in rpc.listpeers()['peers']
            if p['channels'] and
            Amount(p['channels'][0]['msatoshi_total'], 'msat') <= amount]


# List all connected peers with channels
def peers_no_channel(rpc):
    return [p for p in rpc.listpeers()['peers']
            if not p['channels']]


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
    if filter_name.lower() == 'nochannel':
        return peers_no_channel(rpc)
    if filter_name.lower() == 'greater_than':
        amt = Amount(amount, unit)
        return channels_greater_than(rpc, amt)
    if filter_name.lower() == 'less_than':
        amt = Amount(amount, unit)
        return channels_less_than(rpc, amt)
