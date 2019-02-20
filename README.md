# c-lightning-plugins

Work In Progress...

A collection of plugins for c-lightning to do convenient things. Please contribute ideas!

## Usage

Start lightningd with this `plugin-dir` command pointing to this repository
```bash
git clone https://github.com/conscott/c-lightning-plugins.git
cd c-lightning-plugins
export CL_DIR=`pwd`
lightningd --plugin-dir $CL_DIR
```

Alternatively you can add a line to the c-lightning config (~/.lightning/config)
```
...
plugin-dir=<path to c-lightning-plugins>
...
```

## RPC Commands

* `balance` : Aggregated on-chain balance and channel balance information. Still a work in progress...
* `quickfund`: Use onchain funds to fund `amount` to `num_channels`, simply creating channels with top capacity nodes. This is not recommended for mainnet as it's a bad strategy.
* `closeall` : Close all active channels, with option to force close after timeout
* `getnetworkinfo` : Get statistical information about the current state of the network
* `nodestats` : Get statistical information about a particular node, akin to [1ML](https://1ml.com) stats
* `filter_channels`: Filter channels by various parameters

## Pretty Print
To pretty print the JSON, simply pipe the output to [jq](https://stedolan.github.io/jq/)

```
lightning-cli balance | jq
```

## Future Command Ideas

* Create Circular Route 
* Auto Balance Channels

