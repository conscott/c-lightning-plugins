#!/usr/bin/env python3
from lightning import Plugin
import json
import lib.node_stats
import lib.balance_stats

from lib.amount import is_valid_unit, valid_units

plugin = Plugin(autopatch=True)


@plugin.method("balance")
def balance(plugin, unit='btc'):
    """List detailed onchain and channel balance information
    """
    if not is_valid_unit(unit):
        return "Value units are %s" % ', '.join(valid_units)

    rpc = plugin.rpc

    data = {
        'unit': unit,
        'onchain_total_balance': lib.node_stats.onchain_balance(rpc).to(unit),
        'onchain_confirmed_balance': lib.node_stats.onchain_confirmed_balance(rpc).to(unit),
        'onchain_unconfirmed_balance': lib.node_stats.onchain_unconfirmed_balance(rpc).to(unit),
        'total_funded_outgoing': lib.balance_stats.funded_outgoing_balance(rpc).to(unit),
        'total_funded_incoming': lib.balance_stats.funded_incoming_balance(rpc).to(unit),
        'pending_outgoing_balance': lib.balance_stats.pending_balance(rpc).to(unit),
        'pending_incoming_balance': lib.balance_stats.pending_incoming_balance(rpc).to(unit),
        'active_outgoing_balance': lib.balance_stats.active_balance(rpc).to(unit),
        'active_incoming_balance': lib.balance_stats.active_incoming_balance(rpc).to(unit),
        'closed_recent_to_self': lib.balance_stats.closed_balance(rpc).to(unit),
        'closed_recent_to_remote': lib.balance_stats.closed_incoming_balance(rpc).to(unit),
        'reserve_balance': lib.balance_stats.reserve_balance(rpc).to(unit),
        'spendable_balance': lib.balance_stats.spendable_balance(rpc).to(unit)
    }
    plugin.log(json.dumps(data, indent=2))
    return data


plugin.run()
