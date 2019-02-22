#!/usr/bin/env python3
from lightning import Plugin
import lib.channel_filters import filter_channels

plugin = Plugin(autopatch=True)


@plugin.method("filter_channels")
def filter_channels(plugin, filter_name, amount=0, unit='msat'):
    """Filter channels with `filter_name` as pending, active, closed, greater_than, or less_than with optional
       `amount` and `unit` (msat, sat, mbtc, or btc)
    """
    return filter_channels(plugin.rpc, filter_name, amount, unit)


@plugin.init()
def init(options, configuration, plugin):
    print("Plugin filter_channel.py initialized")


plugin.run()
