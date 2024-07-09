# BIDS-app helper

Helper package to simplify creation of BIDS apps.

## Installation

<!--
Install this package via :

```sh
pip install bidsapp_cli
``` -->

<!-- Or get the newest development version via: -->

Get the newest development version:

```sh
pip install git+https://github.com/kaitj/bidsapp-helper
```

## Quick start

Short tutorial, maybe with a

```Python
from bidsapp_helper.parser import BidsAppArgumentParser

parser = BidsAppArgumentParser(
    app_name="app",
    description="Short description of application"
)
args = parser.parse_args()
```

# Features

- CLI initialization
- Pipeline descriptor

## Links or References

- [BIDS apps](https://bids-apps.neuroimaging.io/about/)
