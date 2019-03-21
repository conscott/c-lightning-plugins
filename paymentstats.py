#!/usr/bin/env python3
from lightning import Plugin
import json
import lib.payment_stats

plugin = Plugin(autopatch=True)


@plugin.method("paymentstats")
def paymentstats(plugin, unit='btc'):
    """List detailed payment stats for local node
    """
    rpc = plugin.rpc
    total_paid = lib.payment_stats.total_payments(rpc).to(unit)
    total_fees = lib.payment_stats.routing_fees_paid(rpc).to(unit)
    percent_fees = round(total_fees / total_paid * 100, 2)
    data = {
        'unit': unit,
        'num_failed_payments': lib.payment_stats.num_failed_payments(rpc),
        'num_complete_payments': lib.payment_stats.num_complete_payments(rpc),
        'total_payments': total_paid,
        'total_payments_sub_routing_fees':  lib.payment_stats.total_payments_no_fees(rpc).to(unit),
        'total_routing_fees': total_fees,
        'percent_paid_in_routing_fees': percent_fees
    }
    plugin.log(json.dumps(data, indent=2))
    return data


plugin.run()
