#!/usr/bin/env python3
from lightning import Plugin

plugin = Plugin(autopatch=True)


@plugin.method("closeall")
def closeall(plugin, force=False, timeout=30):
    """Close all active channels
    """
    # One liner!
    for p in plugin.rpc.listpeers()['peers']:
        for c in p['channels']:
            if c['state'] == 'CHANNELD_NORMAL':
                plugin.log("Closing %s force=%s timeout=%s" % (c['channel_id'], force, timeout))
                plugin.rpc.close(c['channel_id'], force, timeout)
    return "Done."


@plugin.method("init")
def init(options, configuration, plugin):
    print("Plugin closeall.py initialized")

plugin.run()
