from lib.amount import Amount


# All paid invoices
def paid_invoices(rpc):
    return [i for i in rpc.listinvoices()['invoices']
            if i['status'] == 'paid']


# All unpaid invoices
def unpaid_invoices(rpc):
    return [i for i in rpc.listinvoices()['invoices']
            if i['status'] == 'unpaid']


# All expired invoices
def expired_invoices(rpc):
    return [i for i in rpc.listinvoices()['invoices']
            if i['status'] == 'expired']


# Number of paid invoices
def num_paid_invoices(rpc):
    return len(paid_invoices(rpc))


# Number of invoices that are unpaid
def num_unpaid_invoices(rpc):
    return len(unpaid_invoices(rpc))


# Number of invoices that have expired
def num_expired_invoices(rpc):
    return len(expired_invoices(rpc))


# Total in received invoices
def total_received_invoices(rpc):
    return Amount(sum((i['msatoshi_received']
                       for i in paid_invoices(rpc))), 'msat')


# Total in unpaid invoices
def total_unpaid_invoices(rpc):
    return Amount(sum((i['msatoshi']
                       for i in unpaid_invoices(rpc))), 'msat')


# Total in expired invoices
def total_expired_invoices(rpc):
    return Amount(sum((i['msatoshi']
                       for i in expired_invoices(rpc))), 'msat')
