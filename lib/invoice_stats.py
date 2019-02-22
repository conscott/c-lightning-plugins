from amount import Amount

# All paid invoices
def paid_invoices(rpc):
    return [i['msatoshi_received']
            for i in rpc.listinvoices()['invoices']
            if i['status'] == 'paid']


# All unpaid invoices
def unpaid_invoices(rpc):
    return [i['msatoshi_received']
            for i in rpc.listinvoices()['invoices']
            if i['status'] == 'unpaid']


# All expired invoices
def expired_invoices(rpc):
    return [i['msatoshi_received']
            for i in rpc.listinvoices()['invoices']
            if i['status'] == 'expired']

# Total received in invoices
def total_received_invoices(rpc):
    return Amount(sum((i['msatoshi_received']
                       for i in paid_invoices(rpc))), 'msat')


# Total in invoices that have not been paid yet
def total_unpaid_invoices(rpc):
    return Amount(sum((i['msatoshi']
                       for i in unpaid_invoices(rpc))), 'msat')


# Total in invoices that have expired
def total_expired_invoices(rpc):
    return Amount(sum((i['msatoshi']
                       for i in expired_invoices(rpc))), 'msat')
