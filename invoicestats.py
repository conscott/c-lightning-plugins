#!/usr/bin/env python3
from lightning import Plugin
import json
import lib.invoice_stats

plugin = Plugin(autopatch=True)


@plugin.method("invoicestats")
def invoicestats(plugin, unit='btc'):
    """List detailed invoice stats for local node
    """
    rpc = plugin.rpc
    data = {
        'unit': unit,
        'num_paid_invoices': lib.invoice_stats.num_paid_invoices(rpc),
        'num_unpaid_invoices': lib.invoice_stats.num_unpaid_invoices(rpc),
        'num_expired_invoices': lib.invoice_stats.num_expired_invoices(rpc),
        'total_received_invoices': lib.invoice_stats.total_received_invoices(rpc).to(unit),
        'total_unpaid_invoices': lib.invoice_stats.total_unpaid_invoices(rpc).to(unit),
        'total_expired_invoices': lib.invoice_stats.total_expired_invoices(rpc).to(unit),
    }
    plugin.log(json.dumps(data, indent=2))
    return data


plugin.run()
