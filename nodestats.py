#!/usr/bin/env python3
import json
from lightning import Plugin
from plugin_lib import valid_units, is_valid_unit, convert_msat, convert_sat
from statistics import median

plugin = Plugin(autopatch=True)


# A copy of lnd's nodestats rpc command
@plugin.method("nodestats")
def nodestats(plugin, nodeid, unit='btc', verbose=False):
    """Get statistical information about a node's channel
    """

    if len(nodeid) != 66:
        return "Must enter a valid node id"

    if not is_valid_unit(unit):
        return "Value units are %s" % ', '.join(valid_units)

    # Extract public channels for a node
    node_info = plugin.rpc.listnodes(nodeid)['nodes'][0]
    node_channels = [c for c in plugin.rpc.listchannels()['channels'] if c['source'] == nodeid]
    active_channels = [c for c in node_channels if c['active'] == 'true']
    capacity = [c['satoshis'] for c in active_channels]
    fee_rate = [c['fee_per_millionth'] for c in active_channels]
    base_fee = [c['base_fee_millisatoshi'] for c in active_channels]
    num_active_channels = len(active_channels)
    num_closed_channels = len(node_channels) - num_active_channels

    if num_active_channels > 0:
        capacity_sats = sum(capacity)
        capacity_med = median(capacity)
        capacity_avg = capacity_sats / num_active_channels
        fee_rate_med = median(fee_rate)
        fee_rate_avg = sum(fee_rate) / num_active_channels
        base_fee_med = median(base_fee)
        base_fee_avg = sum(base_fee) / num_active_channels
    else:
        capacity_sats = 0
        capacity_med = 0
        capacity_avg = 0
        fee_rate_med = 0
        fee_rate_avg = 0
        base_fee_med = 0
        base_fee_avg = 0

    data = {
        'node': nodeid,
        'alias': node_info['alias'],
        'color': node_info['color'],
        'total_capacity_sat': convert_sat(capacity_sats, unit),
        'active_channels': num_active_channels,
        'closed_channels': num_closed_channels,
        'median_channel_capacity': convert_sat(capacity_med, unit),
        'average_channel_capacity': convert_sat(capacity_avg, unit),
        'median_fee_rate_sat_per_byte': convert_msat(fee_rate_med, unit),
        'average_fee_rate_sat_per_byte': convert_msat(fee_rate_avg, unit),
        'median_base_fee_sat': convert_msat(base_fee_med, unit),
        'average_base_fee_sat': convert_msat(base_fee_avg, unit)
    }

    if verbose:
        data['channels'] = node_channels

    plugin.log(json.dumps(data, indent=4))
    return data


@plugin.method("init")
def init(options, configuration, plugin):
    print("Plugin nodestats.py initialized")


plugin.run()
