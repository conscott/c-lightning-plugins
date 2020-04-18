#!/usr/bin/env python3
from pyln.client import Plugin
import json
import lib.node_stats
import lib.channel_stats

plugin = Plugin()


@plugin.method("channelstats")
def channelstats(plugin):
    """List detailed channel stats for local node
    """
    rpc = plugin.rpc
    data = {
        'num_active_channels': lib.channel_stats.num_active_outgoing(rpc),
        'num_active_outgoing_channels': lib.channel_stats.num_active_outgoing(rpc),
        'num_active_incoming_channels': lib.channel_stats.num_active_incoming(rpc),
        'num_pending_channels': lib.channel_stats.num_pending(rpc),
        'num_pending_outgoing_channels': lib.channel_stats.num_pending_outgoing(rpc),
        'num_pending_incoming_channels': lib.channel_stats.num_pending_incoming(rpc),
        'num_closed_channels': lib.channel_stats.num_closed(rpc),
        'num_closed_outgoing_channels': lib.channel_stats.num_closed_outgoing(rpc),
        'num_closed_incoming_channels': lib.channel_stats.num_closed_incoming(rpc),
        'num_peers_no_channel': lib.channel_stats.num_peers_no_channel(rpc)
    }
    plugin.log(json.dumps(data, indent=2))
    return data


plugin.run()
