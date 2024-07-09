# BIDS-app cli

Helper package to quickly create BIDS-app CLIs.

## Installation

<!--
Install this package via :

```sh
pip install bidsapp_cli
``` -->

<!-- Or get the newest development version via: -->

Get the newest development version:

```sh
pip install git+https://github.com/kaitj/bidsapp-cli
```

## Quick start

Short tutorial, maybe with a

```Python
from bidsapp_cli.parser import BidsAppArgumentParser

parser = BidsAppArgumentParser(
    app_name="app",
    description="Short description of application"
)
args = parser.parse_args()
```

## Links or References

- [BIDS apps](https://bids-apps.neuroimaging.io/about/)
