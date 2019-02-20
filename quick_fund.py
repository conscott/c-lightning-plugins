#!/usr/bin/env python3
from lightning import Plugin
import plugin_lib as lib
import inspect

plugin = Plugin(autopatch=True)


@plugin.method("quickfund")
def quickfund(plugin, amount_sat, num_channels):
    """Automatically create num_channels of amount_sat with top capacity nodes.
       Only recommended for testnet, as it's not the best channel connection strategy.
    """
    # FAIL
    if num_channels is inspect._empty:
        return "Need to specify `num_channels` args"
    if amount_sat is inspect._empty:
        return "Need to specify `amount_sat` args"
    if amount_sat < 50000:
        return "Recommended to create channels with at least 50000 sat"
    if amount_sat > lib.NO_WUMBO:
        return "Cannot create channels larger than %s sat for now" % lib.NO_WUMBO

    # Funds available to add to channel
    onchain_value = lib.onchain_sat(plugin.rpc)
    if onchain_value < (amount_sat * num_channels):
        return ("Total funds required for %s channels of %s sat = %s, "
                "Only have %s sat funds available"
                % (num_channels, amount_sat, amount_sat * num_channels, onchain_value))

    # If node already has outgoing connections to some peers, it should to ignore them
    out_peers = [p['id'] for p in lib.outgoing_channels(plugin.rpc)]

    # Top N capacity channels ignoring those the node already has an open
    # outgoing channel with
    top_cap = lib.top_n_capacity(plugin.rpc, num_channels, ignore=out_peers)

    for chan in top_cap:
        plugin.log("Funding channel %s with %s sat" % (chan, amount_sat))
        #plugin.rpc.connect(chan['node_id'])
        #plugin.rpc.fundchannel(chan['node_id'], amount_sat)

    return "Succes!"


plugin.run()
