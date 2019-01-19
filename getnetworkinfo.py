#!/usr/bin/env python3
import json
from collections import defaultdict
from lightning import Plugin
from statistics import median

plugin = Plugin(autopatch=True)


# A copy of lnd's getnetworkinfo rpc command
@plugin.method("getnetworkinfo")
def getnetworkinfo(plugin, force=False, timeout=30):
    """Get statistical information about the current state of the network.
    """
    nodes = plugin.rpc.listnodes()['nodes']
    channels = plugin.rpc.listchannels()['channels']

    # Graph stats
    graph = defaultdict(list)
    for c in channels:
        graph[c['source']].append(c['destination'])

    chan = 0
    unique = defaultdict(dict)
    for source, destinations in graph.items():
        for d in destinations:
            if d not in unique or source not in unique[d]:
                unique[source][d] = 1
                chan += 1

    num_nodes = len(nodes)
    num_channels = chan

    channel_sat = [c['satoshis'] for c in channels]
    base_fee_msat = [c['base_fee_millisatoshi'] for c in channels]
    fee_rate = [c['fee_per_millionth'] for c in channels]

    # Each channel is counted twice, must divide by two
    total_capacity = sum(channel_sat) / 2
    min_channel_size = min(channel_sat)
    max_channel_size = max(channel_sat)
    med_channel_size = median(channel_sat)
    avg_channel_size = total_capacity / num_channels

    min_base_fee = min(base_fee_msat)
    max_base_fee = max(base_fee_msat)
    med_base_fee = median(base_fee_msat)
    avg_base_fee = sum(base_fee_msat) / len(base_fee_msat)

    min_fee_rate = min(fee_rate)
    max_fee_rate = max(fee_rate)
    med_fee_rate = median(fee_rate)
    avg_fee_rate = sum(fee_rate) / len(fee_rate)

    channels_per_node = [len(v) for k, v in graph.items()]
    max_chan = max(channels_per_node)
    med_chan = median(channels_per_node)
    avg_chan = sum(channels_per_node) / len(channels_per_node)

    data = {
        'num_nodes': num_nodes,
        'num_channels': num_channels,
        'total_network_capacity_btc': total_capacity / 10**8.0,
        'avg_channels_per_node': avg_chan,
        'med_channels_per_node': med_chan,
        'max_channels_per_node': max_chan,
        'min_channel_size_sat': min_channel_size,
        'max_channel_size_sat': max_channel_size,
        'median_channel_size_sat': med_channel_size,
        'avg_channel_size_sat': avg_channel_size,
        'min_base_fee_msat': min_base_fee,
        'max_base_fee_msat': max_base_fee,
        'median_base_fee_msat': med_base_fee,
        'avg_base_fee_msat': avg_base_fee,
        'min_fee_rate_msat': min_fee_rate,
        'max_fee_rate_msat': max_fee_rate,
        'median_fee_rate_msat': med_fee_rate,
        'avg_fee_rate_msat': avg_fee_rate
    }
    plugin.log(json.dumps(data, indent=4))

    return data


@plugin.method("init")
def init(options, configuration, plugin):
    print("Plugin getnetworkinfo.py initialized")


plugin.run()
