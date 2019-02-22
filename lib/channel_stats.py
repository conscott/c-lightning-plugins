from amount import Amount
from channel_filters import (
        pending_channels, active_channels,
        closed_channels, incoming_channels,
        outgoing_channels, active_incoming_channels,
        active_outgoing_channels, pending_incoming_channels,
        pending_outgoing_channels, closed_incoming_channels,
        closed_outgoing_channels, channels_greater_than,
        channels_less_than, peers_no_channel)


# The number of incoming channels
def num_incoming_channels(rpc):
    return len(incoming_channels(rpc))


# The number of outgoing channels
def num_outgoing_channels(rpc):
    return len(outgoing_channels(rpc))


# Number of pending channels
def num_pending(rpc):
    return len(pending_channels(rpc))


# Number of pending outgoing channels
def num_pending_outgoing(rpc):
    return len(pending_outgoing_channels(rpc))


# Number of pending incoming channels
def num_pending_incoming(rpc):
    return len(pending_incoming_channels(rpc))


# Number of active channels
def num_active(rpc):
    return len(active_channels(rpc))


# Number of active outgoing channels
def num_active_outgoing(rpc):
    return len(active_outgoing_channels(rpc))


# Number of active incoming channels
def num_active_incoming(rpc):
    return len(active_incoming_channels(rpc))


# Number of closed channels
def num_closed(rpc):
    return len(closed_channels(rpc))


# Number of closed outgoing channels
def num_closed_outgoing(rpc):
    return len(closed_outgoing_channels(rpc))


# Number of closed incoming channels
def num_closed_incoming(rpc):
    return len(closed_incoming_channels(rpc))


# Number of closed incoming channels
def num_peers_no_channel(rpc):
    return len(peers_no_channel(rpc))


# Number of channels with value greater than Amount
def num_greather_than(rpc, amount):
    assert type(amount) is Amount
    return len(channels_greater_than(rpc, amount))


# Number of channels with value greater than Amount
def num_less_than(rpc, amount):
    assert type(amount) is Amount
    return len(channels_less_than(rpc, amount))
