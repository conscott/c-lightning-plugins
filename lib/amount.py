valid_units = (
    'msat',
    'sat',
    'mbtc',
    'btc'
)

msat_convert = {
    'msat': 1.0,
    'sat': 1000.0,
    'mbtc': 10**8.0,
    'btc': 10**11.0
}

sat_convert = {
    'msat': 0.001,
    'sat': 1.0,
    'mbtc': 10**5.0,
    'btc': 10**8.0
}

mbtc_convert = {
    'msat': 10**8.0,
    'sat': 10**5.0,
    'mbtc': 1.0,
    'btc': 0.001
}

btc_convert = {
    'msat': 10**11.0,
    'sat': 10**8.0,
    'mbtc': 1000.0,
    'btc': 1.0
}

convert_any = {
    'msat': msat_convert,
    'sat': sat_convert,
    'mbtc': mbtc_convert,
    'btc': btc_convert
}


class Amount():

    def __init__(self, amount, unit):

        if not is_valid_unit(unit):
            raise ValueError("Invalid btc unit %s, must be in %s" % (unit, valid_units))

        self._amt = amount
        self._unit = unit.lower()

    def to(self, to_unit):
        return (self._amt * convert_any[self._unit][to_unit])

    def __str__(self):
        return "Amount: %s %s" % (self._amt, self._unit)

    def __add__(self, other):
        return self.__class__(self._amt + other.to(self._unit), self._unit)

    def __sub__(self, other):
        return self.__class__(self._amt - other.to(self._unit), self._unit)

    def __eq__(self, other):
        return self._amt == other.to(self._unit)

    def __ne__(self, other):
        return self._amt != other.to(self._unit)

    def __lt__(self, other):
        return self._amt < other.to(self._unit)

    def __le__(self, other):
        return self._amt <= other.to(self._unit)

    def __gt__(self, other):
        return self._amt > other.to(self._unit)

    def __ge__(self, other):
        return self._amt >= other.to(self._unit)


def is_valid_unit(unit):
    return unit.lower() in valid_units


def convert_msat(val, unit):
    return val / msat_convert[unit.lower()]


def convert_sat(val, unit):
    return val / sat_convert[unit.lower()]


def convert_mbtc(val, unit):
    return val / mbtc_convert[unit.lower()]


def convert_btc(val, unit):
    return val / btc_convert[unit.lower()]
