#!/usr/bin/env python3
#from lightning import Plugin
from lightning import LightningRpc
import plugin_lib as lib
import os

#plugin = Plugin(autopatch=True)

def default_configdir():
    home = os.getenv("HOME")
    if home:
        return os.path.join(home, ".lightning")
    return "."

rpc_path = os.path.join(default_configdir(), "lightning-rpc")
rpc = LightningRpc(rpc_path)

print("Incoming channels...")
print("Capacity\tIncoming\t50/50\tCurrent Ratio")
incoming_channels = lib.incoming_channels(rpc)
for idx, c in enumerate(incoming_channels):
    avail_incoming = c['msatoshi_total'] - c['msatoshi_to_us']
    fifty_fifty = c['msatoshi_total'] / 2
    current_ratio = (avail_incoming / c['msatoshi_total']) * 100
    print("%s:%s\t%s\t%s\t%s" % (idx, c['msatoshi_total'], avail_incoming, fifty_fifty, current_ratio))

print("Outgoing channels...")
print("Capacity\tOutgoing\t50/50\tCurrent Ratio")
outgoing_channels = lib.outgoing_channels(rpc)
for idx, c in outgoing_channels:
    avail_outgoing = c['msatoshi_total'] - c['msatoshi_to_us']
    fifty_fifty = c['msatoshi_total'] / 2
    current_ratio = avail_outgoing / c['msatoshi_total'] * 100
    print("%s:%s\t%s\t%s\t%s" % (idx, c['msatoshi_total'], avail_outcoming, fifty_fifty, current_ratio))


in_num = input("\nPick Incoming Route")
ot_num = input("\nPick Outgoing Route")
amt = input("\nPick amount (sat) to rebalance")

route = rpc.getroute(incoming_channels[in_num]['id'], sat, 1.0)
route.append({
    "id": lib.get_nodeid(rpc),
    "channel": incoming_channels[in_num]['channels'][0]['short_channel_id'],
    "msatoshi": msatoshi,
    "deplay": 1
})

rpc.sendpay(route,...)
