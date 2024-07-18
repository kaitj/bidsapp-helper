"""Parser-creator."""

import pathlib as pl
from argparse import ArgumentParser, FileType
from collections.abc import Sequence
from typing import Any, Callable, overload

import yaml


class BidsAppArgumentParser(ArgumentParser):
    """Representation of BIDS app CLI."""

    def __init__(self, app_name: str, description: str, *args, **kwargs) -> None:
        super().__init__(  # type: ignore
            prog=app_name,
            usage="%(prog)s bids_dir output_dir analysis_level [options]",
            description=description,
            *args,
            **kwargs,
        )
        self._add_common_args()

    def _add_common_args(self) -> None:
        self.add_argument(
            "bids_dir",
            action="store",
            type=pl.Path,
            help="dataset directory (bids + derivatives)",
        )
        self.add_argument(
            "output_dir", action="store", type=pl.Path, help="output directory"
        )
        self.add_argument(
            "analysis_level",
            metavar="analysis_level",
            type=str,
            choices=["participant"],  # Initial choices
            help="{%(choices)s}",
        )

    def _get_arg_type(self, key: str) -> Callable[[str], Any] | FileType | None:
        """Retrieve argument type based on its key."""
        for action in self._actions:
            if action.dest == key:
                return action.type
        raise KeyError("Unable to find configuration key")

    def generate_config(self) -> dict[str, Any]:
        """Generate config dict."""
        config = {}
        for action in self._actions:
            if action.dest not in {"help", "version"}:
                try:
                    config[action.dest] = action.type(action.default)  # type: ignore
                except Exception:
                    config[action.dest] = action.default
        return config

    def load_config(self, config: dict[str, Any], config_fpath: pl.Path) -> None:
        """Load arguments from configuration file."""
        if (config_fpath := pl.Path(config_fpath)).suffix not in [".yaml", ".yml"]:
            raise ValueError("Please provide a YAML configuration file")

        if config_fpath.exists():
            with open(config_fpath, "r") as config_file:
                updated_attrs = yaml.safe_load(config_file)

            for key, val in updated_attrs.items():
                config[key] = self._get_arg_type(key)(val)  # type: ignore

    @overload  # type: ignore
    def parse_args(self, *args, config: dict[str, Any], **kwargs) -> None: ...

    @overload
    def parse_args(self, *args, config: None, **kwargs) -> dict[str, Any]: ...

    def parse_args(self, *args, config: dict[str, Any] | None, **kwargs):
        """Parse arguments into config dict."""
        args = vars(super().parse_args(*args, **kwargs))
        if config:
            for key, val in args.items():  # type: ignore
                config[key] = val
        else:
            return args

    def update_analysis_level(self, choices: Sequence[str]) -> None:
        """Update analysis-level choices."""
        for action in self._actions:
            if action.dest == "analysis_level":
                action.choices = choices
                return
