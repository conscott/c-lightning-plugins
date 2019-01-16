# c-lightning-plugins

Work In Progress...

A collection of plugins for c-lightning to do convenient things.

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
```


## Added RPC Commands

* `balance` : Aggregated on-chain balance and channel balance information. Still a work in progress...
* `closeall` : Close all active channels, with option to force close after timeout
* `getnetworkinfo` : Get statistical information about the current state of the network
