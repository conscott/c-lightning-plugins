#!/usr/bin/env python3
from pyln.client import Plugin

plugin = Plugin()


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


plugin.run()
