#!/usr/bin/env python3
import json
from lightning import Plugin
from statistics import median

plugin = Plugin(autopatch=True)


# A copy of lnd's nodestats rpc command
@plugin.method("nodestats")
def nodestats(plugin, node, verbose=False):
    """Get statistical information about the current state of the network.
    """

    # Extract public channels for a node
    node_info = plugin.rpc.listnodes(node)['nodes'][0]
    node_channels = [c for c in plugin.rpc.listchannels()['channels'] if c['source'] == node]
    num_active_channels = len([c for c in node_channels if c['active'] is True])
    num_closed_channels = len(node_channels) - num_active_channels
    capacity = [c['satoshis'] for c in node_channels if c['active'] is True]
    fee_rate = [c['fee_per_millionth'] for c in node_channels if c['active'] is True]
    base_fee = [c['base_fee_millisatoshi'] for c in node_channels if c['active'] is True]

    capacity_sats = sum(capacity)
    capacity_med = median(capacity)
    capacity_avg = capacity_sats / num_active_channels

    fee_rate_med = median(fee_rate)
    fee_rate_avg = sum(fee_rate) / num_active_channels

    base_fee_med = median(base_fee)
    base_fee_avg = sum(base_fee) / num_active_channels

    data = {
        'node': node,
        'alias': node_info['alias'],
        'color': node_info['color'],
        'total_capacity_sat': capacity_sats,
        'active_channels': num_active_channels,
        'closed_channels': num_closed_channels,
        'median_channel_capacity': capacity_med,
        'average_channel_capacity': capacity_avg,
        'median_fee_rate_sat_per_byte': fee_rate_med,
        'average_fee_rate_sat_per_byte': fee_rate_avg,
        'median_base_fee_sat': base_fee_med,
        'average_base_fee_sat': base_fee_avg
    }

    if verbose:
        data['channels'] = node_channels

    plugin.log(json.dumps(data, indent=4))
    return data


@plugin.method("init")
def init(options, configuration, plugin):
    print("Plugin nodestats.py initialized")


plugin.run()
