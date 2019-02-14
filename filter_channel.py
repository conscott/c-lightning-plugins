#!/usr/bin/env python3
from lightning import Plugin
from plugin_lib import (valid_units, channel_filters,
                        is_valid_unit, is_valid_filter,
                        convert_msat, get_nodeid,
                        channel_pending, channel_active, channel_closed)

plugin = Plugin(autopatch=True)


@plugin.method("filter_channels")
def filter_channels(plugin, filter_name, amount=0, unit='sat'):

    """Filter channels as "pending", "active", "closed", "greater_than", "less_than" with optional
       `amount` and `unit` ("msat", "sat", "mbtc", or "btc")
    """
    if not is_valid_filter(filter_name):
        return "Value filter_name's are %s" % ', '.join(channel_filters)

    if filter_name.lower() == 'pending':
        return [p['channels'][0] for p in plugin.rpc.listpeers()['peers']
                if channel_pending(p['channels'][0]['state'])]
    if filter_name.lower() == 'active':
        return [p['channels'][0] for p in plugin.rpc.listpeers()['peers']
                if channel_active(p['channels'][0]['state'])]
    if filter_name.lower() == 'closed':
        return [p['channels'][0] for p in plugin.rpc.listpeers()['peers']
                if channel_closed(p['channels'][0]['state'])]
    if filter_name.lower() == 'incoming':
        return [p['channels'][0] for p in plugin.rpc.listpeers()['peers']
                if p['channels'][0]['funding_allocation_msat'][get_nodeid(plugin.rpc)] <= 0]
    if filter_name.lower() == 'outgoing':
        return [p['channels'][0] for p in plugin.rpc.listpeers()['peers']
                if p['channels'][0]['funding_allocation_msat'][get_nodeid(plugin.rpc)] > 0]

    # Filter based on channel capacity
    if not is_valid_unit(unit):
        return "Value units are %s" % ', '.join(valid_units)

    if filter_name.lower() == 'greater_than':
        return [p['channels'][0] for p in plugin.rpc.listpeers()['peers']
                if convert_msat(p['channels'][0]['msatoshi_total'], unit) >= amount]
    if filter_name.lower() == 'less_than':
        return [p['channels'][0] for p in plugin.rpc.listpeers()['peers']
                if convert_msat(p['channels'][0]['msatoshi_total'], unit) <= amount]


@plugin.init()
def init(options, configuration, plugin):
    print("Plugin filter_channel.py initialized")


plugin.run()
