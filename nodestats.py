#!/usr/bin/env python3
import json
from lightning import Plugin

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
    capacity_sats = sum((c['satoshis'] for c in node_channels))

    data = {
        'node': node,
        'alias': node_info['alias'],
        'color': node_info['color'],
        'capacity_sat': capacity_sats,
        'active_channels': num_active_channels,
        'closed_channels': num_closed_channels,
    }
    if verbose:
        data['channels'] = node_channels
    plugin.log(json.dumps(data, indent=4))
    return data


@plugin.method("init")
def init(options, configuration, plugin):
    print("Plugin nodestats.py initialized")


plugin.run()
