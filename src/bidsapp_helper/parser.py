"""Parser-creator."""

import pathlib as pl
from argparse import ArgumentParser, Namespace
from typing import Sequence


class BidsAppArgumentParser:
    """BIDS-app CLI parser."""

    def __init__(self, app_name: str, description: str) -> None:  # noqa: D107
        self.parser = ArgumentParser(
            prog=app_name,
            usage="%(prog)s bids_dir output_dir analysis_level [options]",
            description=f"""
            {description}
            """,
        )
        self._add_common_args()

    def _add_common_args(self) -> None:
        """Common bids arguments."""
        self.parser.add_argument(
            "bids_dir", action="store", type=pl.Path, help="path to BIDS dataset"
        )

        self.parser.add_argument(
            "output_dir",
            action="store",
            type=pl.Path,
            help="path to output directory",
        )
        self.parser.add_argument(
            "analysis_level",
            metavar="analysis_level",
            type=str,
            choices=["participant"],  # Initial choices
            help="analysis level to be performed",
        )

    def update_analysis_level(self, choices: list[str]) -> None:
        """Helper to update the choices available."""
        for action in self.parser._actions:
            if action.dest == "analysis_level":
                action.choices = choices
                return

    def parse_args(self, args: Sequence[str] | None = None) -> Namespace:
        """Parse CLI arguments."""
        return self.parser.parse_args(args)
