#!/usr/bin/env python3
from lightning import Plugin
import json
from plugin_lib import channel_pending, channel_active

plugin = Plugin(autopatch=True)

# Can return values as these units
valid_units = ['msat', 'sat', 'mbtc', 'btc']

sat_convert = {
    'msat': 1000.0,
    'sat': 1.0,
    'mbtc': 10**5.0,
    'btc': 10**8.0
}

msat_convert = {
    'msat': 1.0,
    'sat': 1000.0,
    'mbtc': 10**8.0,
    'btc': 10**11.0
}


# Change msat to unit
def convert_msat(val, unit):
    return val / msat_convert[unit]


# Change sat to unit
def convert_sat(val, unit):
    return val / sat_convert[unit]


@plugin.method("balance")
def balance(plugin, unit='btc'):
    """List detailed onchain and channel balance information
    """
    unit = unit.lower()
    if unit not in valid_units:
        return "Value units are %s" % ', '.join(valid_units)

    funds = plugin.rpc.listfunds()
    peerinfo = plugin.rpc.listpeers()
    payments = plugin.rpc.listpayments()
    invoices = plugin.rpc.listinvoices()
    node_id = plugin.rpc.getinfo()['id']

    # Funds available to add to channel
    onchain_value = sum([int(x["value"]) for x in funds["outputs"]])

    pending_incoming, pending_outgoing = 0, 0
    active_incoming, active_outgoing = 0, 0
    closed_incoming, closed_outgoing = 0, 0
    initial_incoming, initial_outgoing = 0, 0
    num_incoming, num_outgoing = 0, 0
    num_pend_incoming, num_pend_outgoing = 0, 0
    num_active_incoming, num_active_outgoing = 0, 0
    num_closed_incoming, num_closed_outgoing = 0, 0
    reserve_balance = 0
    for p in peerinfo['peers']:
        for channel in p['channels']:
            # Channel is incoming if our node didn't fund the channel
            incoming = channel['funding_allocation_msat'][node_id] == 0
            if incoming:
                num_incoming += 1
                initial_incoming += channel['msatoshi_total']
            else:
                num_outgoing += 1
                initial_outgoing += channel['msatoshi_total']

            if channel_pending(channel['state']):
                pending_outgoing += channel['msatoshi_to_us']
                pending_incoming += channel['msatoshi_total'] - channel['msatoshi_to_us']
                if incoming:
                    num_pend_incoming += 1
                else:
                    num_pend_outgoing += 1
            elif channel_active(channel['state']):
                reserve_balance += channel['our_channel_reserve_satoshis']
                active_outgoing += channel['msatoshi_to_us']
                active_incoming += channel['msatoshi_total'] - channel['msatoshi_to_us']
                if incoming:
                    num_active_incoming += 1
                else:
                    num_active_outgoing += 1
            else:
                closed_incoming += channel['msatoshi_total'] - channel['msatoshi_to_us']
                closed_outgoing += channel['msatoshi_to_us']
                if incoming:
                    num_closed_incoming += 1
                else:
                    num_closed_outgoing += 1

    paid = sum([p['msatoshi'] for p in payments['payments'] if p['status'] == 'complete'])
    paid_w_fees = sum([p['msatoshi_sent'] for p in payments['payments'] if p['status'] == 'complete'])
    fees = sum([(p['msatoshi_sent'] - p['msatoshi']) for p in payments['payments'] if p['status'] == 'complete'])
    received = sum([i['msatoshi_received'] for i in invoices['invoices'] if i['status'] == 'paid'])

    data = {
        'unit': unit,
        'onchain_balance': convert_sat(onchain_value, unit),
        'num_pending_outgoing_channels': num_pend_outgoing,
        'num_pending_incoming_channels': num_pend_incoming,
        'num_active_outgoing_channels': num_active_outgoing,
        'num_active_incoming_channels': num_active_incoming,
        'num_closed_outgoing_channels': num_closed_outgoing,
        'num_closed_incoming_channels': num_closed_incoming,
        'total_funded_outgoing': convert_msat(initial_outgoing, unit),
        'total_funded_incoming': convert_msat(initial_incoming, unit),
        'pending_outgoing_balance': convert_msat(pending_outgoing, unit),
        'pending_incoming_balance': convert_msat(pending_incoming, unit),
        'active_outgoing_balance': convert_msat(active_outgoing, unit),
        'active_incoming_balance': convert_msat(active_incoming, unit),
        'closed_recent_to_self': convert_msat(closed_outgoing, unit),
        'closed_recent_to_remote': convert_msat(closed_incoming, unit),
        'reserve_balance':  convert_msat(reserve_balance, unit),
        'spendable_balance': convert_msat(active_outgoing - reserve_balance, unit),
        'total_invoices_paid': convert_msat(paid, unit),
        'total_routing_fees_paid': convert_msat(fees, unit),
        'total_paid_with_routing': convert_msat(paid_w_fees, unit),
        'total_received_invoices': convert_msat(received, unit)
    }
    plugin.log(json.dumps(data, indent=2))
    return data


@plugin.method("init")
def init(options, configuration, plugin):
    print("Plugin balance.py initialized")

plugin.run()
