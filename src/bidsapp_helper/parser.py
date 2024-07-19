"""Parser-creator."""

import argparse
import pathlib as pl
from collections.abc import Sequence
from typing import Any, Callable

import yaml


class BidsAppArgumentParser(argparse.ArgumentParser):
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
            help="path to dataset directory (bids + derivatives)",
        )
        self.add_argument(
            "output_dir", action="store", type=pl.Path, help="path to output directory"
        )
        self.add_argument(
            "analysis_level",
            metavar="analysis_level",
            type=str,
            choices=["participant"],  # Initial choices
            help="{%(choices)s}",
        )
        self.add_argument(
            "--config",
            action="store",
            type=pl.Path,
            help="path to app config file",
        )

    def _get_arg_type(
        self, key: str
    ) -> Callable[[str], Any] | argparse.FileType | None:
        """Retrieve argument type based on its key."""
        for action in self._actions:
            if action.dest == key:
                return bool if isinstance(action.const, bool) else action.type
        raise KeyError("Unable to find configuration key")

    def _generate_config(self) -> None:
        """Generate config dict."""
        self.config = {}
        for action in self._actions:
            if action.dest not in {"help", "version"}:
                try:
                    self.config[action.dest] = action.type(action.default)  # type: ignore
                except Exception:
                    self.config[action.dest] = action.default

    def _load_config(self, config_fpath: pl.Path) -> None:
        """Load arguments from configuration file."""
        if (config_fpath := pl.Path(config_fpath)).suffix not in [".yaml", ".yml"]:
            raise ValueError("Please provide a YAML configuration file")

        if config_fpath.exists():
            with open(config_fpath, "r") as config_file:
                updated_attrs = yaml.safe_load(config_file)

            for key, val in updated_attrs.items():
                if key in {"config"}:
                    continue
                self.config[key] = self._get_arg_type(key)(val)  # type: ignore

    def parse_args(self, *args, **kwargs) -> dict[str, Any]:  # type: ignore
        """Parse arguments into config dict."""
        self._generate_config()
        args = vars(super().parse_args(*args, **kwargs))
        assert isinstance(args, dict)

        if not (config_fpath := args.get("config")):
            return args

        self._load_config(config_fpath=config_fpath)
        for key, val in args.items():  # type: ignore
            if val and self.get_default(key) != val:
                self.config[key] = val

        return self.config

    def update_analysis_level(self, choices: Sequence[str]) -> None:
        """Update analysis-level choices."""
        for action in self._actions:
            if action.dest == "analysis_level":
                action.choices = choices
                return
