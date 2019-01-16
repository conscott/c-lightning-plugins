#!/usr/bin/env python3
from lightning import Plugin
import json

from plugin_lib import channel_pending, channel_active

plugin = Plugin(autopatch=True)

M = 10**3.0
COIN = 10**8.0
MCOIN = 10**11.0


@plugin.method("balance")
def balance(plugin):
    """List detailed onchain and channel balance information
    """
    funds = plugin.rpc.listfunds()
    peerinfo = plugin.rpc.listpeers()
    payments = plugin.rpc.listpayments()
    invoices = plugin.rpc.listinvoices()
    node_id = plugin.rpc.getinfo()['id']

    onchain_value = sum([int(x["value"]) for x in funds["outputs"]])

    pending_incoming, pending_outgoing = 0, 0
    active_incoming, active_outgoing = 0, 0
    closed_incoming, closed_outgoing = 0, 0
    initial_incoming, initial_outgoing = 0, 0
    reserve_balance = 0
    num_incoming = 0
    num_outgoing = 0
    for p in peerinfo['peers']:
        for channel in p['channels']:
            # Channel is incoming if our node didn't fund the channel
            incoming = channel['funding_allocation_msat'][node_id] == 0
            if incoming:
                num_incoming += 1
                initial_incoming += channel['msatoshi_total']
                if channel_pending(channel['state']):
                    pending_incoming += channel['msatoshi_total'] - channel['msatoshi_to_us']
                elif channel_active(channel['state']):
                    active_incoming += channel['msatoshi_total'] - channel['msatoshi_to_us']
                else:
                    closed_incoming += channel['msatoshi_total'] - channel['msatoshi_to_us']
            else:
                num_outgoing += 1
                initial_outgoing += channel['msatoshi_total']
                reserve_balance += channel['our_channel_reserve_satoshis']
                if channel_pending(channel['state']):
                    pending_outgoing += channel['msatoshi_to_us']
                elif channel_active(channel['state']):
                    active_outgoing += channel['msatoshi_to_us']
                else:
                    closed_outgoing += channel['msatoshi_to_us']

    paid = sum([p['msatoshi'] for p in payments['payments'] if p['status'] == 'complete'])
    paid_w_fees = sum([p['msatoshi_sent'] for p in payments['payments'] if p['status'] == 'complete'])
    fees = sum([(p['msatoshi_sent'] - p['msatoshi']) for p in payments['payments'] if p['status'] == 'complete'])
    received = sum([i['msatoshi_received'] for i in invoices['invoices'] if i['status'] == 'paid'])

    data = {
        'onchain_balance': '{0:.11f}'.format(onchain_value / COIN),
        'num_outgoing_channels': num_outgoing,
        'num_incoming_channels': num_incoming,
        'funded_outgoing': initial_outgoing / MCOIN,
        'funded_incoming': initial_incoming / MCOIN,
        'pending_outgoing': pending_outgoing / MCOIN,
        'pending_incoming': pending_incoming / MCOIN,
        'active_outgoing': active_outgoing / MCOIN,
        'active_incoming': active_incoming / MCOIN,
        'closed_outgoing': closed_outgoing / MCOIN,
        'closed_incoming': closed_incoming / MCOIN,
        'reserve_balance':  '{0:.11f}'.format(reserve_balance / MCOIN),
        'spendable_balance': '{0:.11f}'.format((active_outgoing - reserve_balance) / MCOIN),
        'total_invoices_paid': '{0:.11f}'.format(paid / MCOIN),
        'total_routing_fees_paid': '{0:.11f}'.format(fees / MCOIN),
        'total_paid_with_routing': '{0:.11f}'.format(paid_w_fees / MCOIN),
        'total_received_invoices': '{0:.11f}'.format(received / MCOIN)
    }
    plugin.log(json.dumps(data, indent=4))
    return data


@plugin.method("init")
def init(options, configuration, plugin):
    print("Plugin balance.py initialized")

plugin.run()
