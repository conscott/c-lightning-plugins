# Can return values as these units
valid_units = ['msat', 'sat', 'mbtc', 'btc']
channel_filters = ['pending', 'active', 'closed', 'incoming', 'outgoing', 'greater_than', 'less_than']

sat_convert = {
    'msat': 0.001,
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


def get_nodeid(rpc):
    return rpc.getinfo()['id']


def is_valid_unit(unit):
    return unit.lower() in valid_units


def is_valid_filter(f):
    return f.lower() in channel_filters


def convert_msat(val, unit):
    return val / msat_convert[unit.lower()]


def convert_sat(val, unit):
    return val / sat_convert[unit.lower()]


def channel_pending(state):
    return state == 'CHANNELD_AWAITING_LOCKIN'


def channel_active(state):
    return (state != 'FUNDING_SPEND_SEEN' and
            state != 'CLOSINGD_COMPLETE' and
            state != 'ONCHAIN')


def channel_closed(state):
    return not (channel_pending(state) or channel_active(state))
