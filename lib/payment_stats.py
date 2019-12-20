from lib.amount import Amount


def payments(rpc):
    try:
        return rpc.listpayments()['payments']
    except Exception:
        try:
            return rpc.listpays()['pays']
        except Exception:
            pass
    return []


# Failed payments
def failed_payments(rpc):
    return [p for p in payments(rpc)
            if p['status'] == 'failed']


# All complete payments
def complete_payments(rpc):
    return [p for p in payments(rpc)
            if p['status'] == 'complete']


# Total number of failed payments
def num_failed_payments(rpc):
    return len(failed_payments(rpc))


# Total number of complete payments
def num_complete_payments(rpc):
    return len(complete_payments(rpc))


# Total routing fees paid thus far on node
def routing_fees_paid(rpc):
    return Amount(sum((p['msatoshi_sent'] - p['msatoshi']
                       for p in complete_payments(rpc))), 'msat')


# Total in sent payments
def total_payments(rpc):
    return Amount(sum((p['msatoshi_sent']
                       for p in complete_payments(rpc))), 'msat')


# Total in sent payments
def total_payments_no_fees(rpc):
    return Amount(sum((p['msatoshi']
                       for p in complete_payments(rpc))), 'msat')
