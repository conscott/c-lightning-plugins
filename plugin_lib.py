def channel_pending(state):
    return state == 'CHANNELD_AWAITING_LOCKIN'


def channel_active(state):
    return (state != 'FUNDING_SPEND_SEEN' and
            state != 'CLOSINGD_COMPLETE' and
            state != 'ONCHAIN')
