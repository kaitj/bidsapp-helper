"""Unit test for testing CLI parser."""

import pathlib as pl

import pytest

from bidsapp_helper.parser import BidsAppArgumentParser


@pytest.fixture
def parser() -> BidsAppArgumentParser:
    return BidsAppArgumentParser(app_name="test_app", description="Test description")


@pytest.fixture
def bids_args() -> list[str]:
    return ["bids_dir", "output_dir", "participant"]


def test_default_cli(parser: BidsAppArgumentParser, bids_args: list[str]):
    args = parser.parse_args(bids_args, config=None)

    assert isinstance(args["bids_dir"], pl.Path)
    assert isinstance(args["output_dir"], pl.Path)
    assert (
        isinstance(args["analysis_level"], str)
        and args["analysis_level"] == "participant"
    )
