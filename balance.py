#!/usr/bin/env python3
from lightning import Plugin
import json

plugin = Plugin(autopatch=True)

M = 10**3.0
COIN = 10**8.0
MCOIN = 10**11.0

@plugin.method("balance")
def balance(plugin, unit):
    """List detailed onchain and channel balance information
    """
    funds = plugin.rpc.listfunds()
    peerinfo = plugin.rpc.listpeers()
    payments = plugin.rpc.listpayments()
    invoices  = plugin.rpc.listinvoices()

    onchain_value = sum([int(x["value"]) for x in funds["outputs"]])
    channel_value = sum([int(x["channel_sat"]) for x in funds["channels"]])
    total_funds = onchain_value + channel_value

    incoming_total_balance = 0
    outgoing_total_balance = 0
    reserve_balance = 0
    for p in peerinfo['peers']:
        for channel in p['channels']:
            incoming_total_balance += (channel['msatoshi_total'] - channel['msatoshi_to_us'])
            outgoing_total_balance += channel['msatoshi_to_us']
            reserve_balance += channel['our_channel_reserve_satoshis']


    paid = sum([p['msatoshi'] for p in payments['payments'] if p['status'] == 'complete'])
    paid_w_fees = sum([p['msatoshi_sent'] for p in payments['payments'] if p['status'] == 'complete'])
    fees = sum([(p['msatoshi_sent'] - p['msatoshi']) for p in payments['payments'] if p['status'] == 'complete'])
    received = sum([i['msatoshi_received'] for i in invoices['invoices'] if i['status'] == 'paid'])

    data = {
        'onchain_balance': '{0:.8f}'.format(onchain_value / COIN),
        'channel_balance': '{0:.8f}'.format(channel_value / COIN),
        'total_balance': '{0:.8f}'.format(total_funds / COIN),
        'outgoing_balance': '{0:.8f}'.format(outgoing_total_balance / MCOIN),
        'reserve_balance':  '{0:.8f}'.format(reserve_balance / MCOIN),
        'spendable_balance': '{0:.8f}'.format((outgoing_total_balance - reserve_balance) / MCOIN),
        'incoming_balance': '{0:.8f}'.format(incoming_total_balance / MCOIN),
        'total_invoices_paid': '{0:.8f}'.format(paid / MCOIN),
        'total_routing_fees_paid': '{0:.8f}'.format(fees / MCOIN),
        'total_paid_with_routing': '{0:.8f}'.format(paid_w_fees / MCOIN),
        'total_received_invoices': '{0:.8f}'.format(received / MCOIN)
    }
    plugin.log(json.dumps(data, indent=4))
    return data

@plugin.method("init")
def init(options, configuration, plugin):
    print("Plugin balance.py initialized")

plugin.run()
