from lib.amount import Amount
from lib.channel_filters import (
        pending_channels, active_channels,
        closed_channels, incoming_channels,
        outgoing_channels)


# Sum local balance of all active channels
def active_balance(rpc):
    return Amount(sum((p['channels'][0]['msatoshi_to_us']
                  for p in active_channels(rpc))), 'msat')


# Sum local balance of all pending channels
def pending_balance(rpc):
    return Amount(sum((p['channels'][0]['msatoshi_to_us']
                       for p in pending_channels(rpc))), 'msat')


# Sum local balance of all closed channels
def closed_balance(rpc):
    return Amount(sum((p['channels'][0]['msatoshi_to_us']
                       for p in closed_channels(rpc))), 'msat')


# Sum remote balance of all active channels
def active_incoming_balance(rpc):
    return Amount(sum((p['channels'][0]['msatoshi_total'] - p['channels'][0]['msatoshi_to_us']
                  for p in active_channels(rpc))), 'msat')


# Sum remote balance of all pending channels
def pending_incoming_balance(rpc):
    return Amount(sum((p['channels'][0]['msatoshi_total'] - p['channels'][0]['msatoshi_to_us']
                  for p in pending_channels(rpc))), 'msat')


# Sum remote balance of all closed channels
def closed_incoming_balance(rpc):
    return Amount(sum((p['channels'][0]['msatoshi_total'] - p['channels'][0]['msatoshi_to_us']
                  for p in closed_channels(rpc))), 'msat')


# Total funded locally
def funded_outgoing_balance(rpc):
    return Amount(sum((p['channels'][0]['msatoshi_total']
                       for p in outgoing_channels(rpc))), 'msat')


# Total funded remotely
def funded_incoming_balance(rpc):
    return Amount(sum((p['channels'][0]['msatoshi_total']
                       for p in incoming_channels(rpc))), 'msat')


# Total local reserve balance
def reserve_balance(rpc):
    return Amount(sum((p['channels'][0]['our_channel_reserve_satoshis']
                       for p in active_channels(rpc))), 'msat')


# Total spendable balance is your active balance - reserve balance
def spendable_balance(rpc):
    return (active_balance(rpc) - reserve_balance(rpc))
