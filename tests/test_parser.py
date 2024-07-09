"""Unit test for testing CLI parser."""

import pathlib as pl

import pytest

from bidsapp_cli.parser import BidsAppArgumentParser


@pytest.fixture
def parser() -> BidsAppArgumentParser:
    return BidsAppArgumentParser(app_name="test_app", description="Test description")


@pytest.fixture
def bids_args() -> list[str]:
    return ["bids_dir", "output_dir", "participant"]


def test_default_cli(parser: BidsAppArgumentParser, bids_args: list[str]):
    args = parser.parse_args(bids_args)

    assert isinstance(args.bids_dir, pl.Path)
    assert isinstance(args.output_dir, pl.Path)
    assert isinstance(args.analysis_level, str) and args.analysis_level == "participant"


@pytest.mark.parametrize(
    "participants",
    [
        (["--participant-label", "01"]),
        (["--participant_label", "sub-01"]),
    ],
)
def test_single_include_participant_label(
    parser: BidsAppArgumentParser, bids_args: list[str], participants: list[str]
):
    bids_args.extend(participants)
    args = parser.parse_args(bids_args)

    assert args.participant_label == "01"
    assert args.exclude_participant_label is None


@pytest.mark.parametrize(
    "participants",
    [
        (["--participant-label", "01, 02, 03"]),
        (["--participant_label", "sub-01 sub-02 sub-03"]),
    ],
)
def test_multiple_include_participant_labels(
    parser: BidsAppArgumentParser, bids_args: list[str], participants: list[str]
):
    """Test multiple inclusion participant-labels."""
    bids_args.extend(participants)
    args = parser.parse_args(bids_args)

    assert args.participant_label == ["01", "02", "03"]
    assert args.exclude_participant_label is None


@pytest.mark.parametrize(
    "participants",
    [
        (["--exclude-participant-label", "01"]),
        (["--exclude_participant_label", "sub-01"]),
    ],
)
def test_single_exclude_participant_label(
    parser: BidsAppArgumentParser, bids_args: list[str], participants: list[str]
):
    bids_args.extend(participants)
    args = parser.parse_args(bids_args)

    assert args.participant_label is None
    assert args.exclude_participant_label == "01"


@pytest.mark.parametrize(
    "participants",
    [
        (["--exclude-participant-label", "01, 02, 03"]),
        (["--exclude_participant_label", "sub-01 sub-02 sub-03"]),
    ],
)
def test_multiple_exclude_participant_labels(
    parser: BidsAppArgumentParser, bids_args: list[str], participants: list[str]
):
    """Test multiple inclusion participant-labels."""
    bids_args.extend(participants)
    args = parser.parse_args(bids_args)

    assert args.participant_label is None
    assert args.exclude_participant_label == ["01", "02", "03"]
