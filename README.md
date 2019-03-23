# c-lightning-plugins

A collection of plugins for c-lightning to do convenient things. At the moment the utilities primarily perform useful filter and aggregation, but the embeded library can be extended for many things.

Please contribute ideas!

## Usage

Start lightningd with the `plugin-dir` option pointing to this repository
```bash
lightningd --plugin-dir <path to this repo>
```

Alternatively you can add a line to the c-lightning config (~/.lightning/config)
```
...
plugin-dir=<path to this repo>
...
```

## RPC Commands

* `balance` : Aggregated on-chain balance and channel balance information. Still a work in progress...
* `nodestats` : Get statistical information about a particular node, akin to [1ML](https://1ml.com) stats
* `channelstats` : Get stats about channels
* `invoicestats` : Get stats about invoices
* `paymentstats` : Get stats about payments
* `quickfund`: Use onchain funds to fund `amount` to `num_channels`, simply creating channels with top capacity nodes. This is not recommended for mainnet as it's a bad strategy.
* `closeall` : Close all active channels, with option to force close after timeout
* `getnetworkinfo` : Get statistical information about the current state of the network
* `filterchannels`: Filter channels by various parameters

## Pretty Print
To pretty print the JSON, simply pipe the output to [jq](https://stedolan.github.io/jq/)

```
lightning-cli balance | jq
```

## Future Command Ideas

* Create Circular Route 
* Auto Balance Channels

