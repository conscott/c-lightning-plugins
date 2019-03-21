#!/usr/bin/env python3
from lib.node_stats import onchain_confirmed_balance, top_n_capacity, WUMBO
from lib.channel_filters import outgoing_channels
from lightning import Plugin

plugin = Plugin(autopatch=True)


@plugin.method("quickfund")
def quickfund(plugin, amount_sat, num_channels):
    """Automatically fund num_channels with amount_sat total connecting to top capacity nodes.
       Only recommended for testnet as this is the worst kind of autopilot.

       Argument amount_sat can be an integer or 'all'
    """
    onchain_value = onchain_confirmed_balance(plugin.rpc).to('sat')
    amount_sat = onchain_value if amount_sat == 'all' else amount_sat

    if not isinstance(amount_sat, int):
        return "Must input integer number or 'all' for amount_sat"

    # Need to save some space for tx fees, this is a total kludge, save
    # 5000 sat per channel for fees of opening
    amount_per_channel = int(amount_sat / num_channels) - 5000

    if amount_per_channel < 50000:
        return ("Funding %s channels with %s sat results in %s sat / channel, "
                "recommended to create channels with at least 50000 sat." %
                (num_channels, amount_sat, amount_per_channel))

    if amount_per_channel > WUMBO.to('sat'):
        return ("Funding %s channels with %s sat results in %s sat / channel, "
                "The current limit is %s sat / channel, need to make more channels" %
                (num_channels, amount_sat, amount_per_channel, WUMBO.to('sat')))

    if onchain_value < amount_sat:
        return "Only have %s sat funds available, channot fund %s" % (amount_sat, onchain_value)

    # If node already has outgoing connections to some peers, it should to ignore them
    out_peers = [p['id'] for p in outgoing_channels(plugin.rpc)]

    # Top N capacity channels ignoring those the node already has an open
    # outgoing channel with
    top_cap = top_n_capacity(plugin.rpc, num_channels + 5, ignore=out_peers)

    num_success = 0
    for chan in top_cap:
        plugin.log("Funding channel %s with %s sat" % (chan, amount_per_channel))
        try:
            plugin.rpc.connect(chan['node_id'])
            plugin.rpc.fundchannel(chan['node_id'], amount_per_channel)
            num_success += 1
            if num_success >= num_channels:
                break
        except Exception as e:
            # If failing to fund, just keep on trying
            plugin.log("Funding channel %s failed... %s" % (chan, str(e)))
            continue

    return "Succes!"


plugin.run()
