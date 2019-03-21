from lib.amount import Amount


# Failed payments
def failed_payments(rpc):
    return [p for p in rpc.listpayments()['payments']
            if p['status'] == 'failed']


# All complete payments
def complete_payments(rpc):
    return [p for p in rpc.listpayments()['payments']
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

