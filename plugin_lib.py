# Can return values as these units
valid_units = ['msat', 'sat', 'mbtc', 'btc']

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


def is_valid_unit(unit):
    return unit.lower() in valid_units


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
