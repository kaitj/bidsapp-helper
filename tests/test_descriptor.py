"""Unit test for descriptor creator"""

import pathlib as pl

import pytest

from bidsapp_helper.descriptor import PipelineDescriptor


@pytest.fixture
def pipeline_descriptor() -> PipelineDescriptor:
    return PipelineDescriptor(app_name="Test App")


def test_descriptor_generation(pipeline_descriptor: PipelineDescriptor):
    descriptor = pipeline_descriptor.descriptor
    assert isinstance(descriptor, dict)
    assert descriptor["Name"] == "Test App"
    assert descriptor["DatasetType"] == "derivative"
    assert descriptor["GeneratedBy"]["Version"] == "0.1.0"
    assert descriptor["GeneratedBy"]["CodeURL"] is None
    assert descriptor["GeneratedBy"]["Author"] is None
    assert descriptor["GeneratedBy"]["AuthorEmail"] is None


def test_invalid_dataset_type():
    with pytest.raises(ValueError, match="Invalid dataset type.*"):
        PipelineDescriptor(app_name="Test App", dataset_type="other")


def test_save_descriptor(
    tmp_path: pl.Path, pipeline_descriptor: PipelineDescriptor
) -> None:
    out_fpath = tmp_path / "pipeline_description.json"
    pipeline_descriptor.save(out_fpath)

    assert out_fpath.exists()


def test_warning_save_descriptor(
    tmp_path: pl.Path,
    pipeline_descriptor: PipelineDescriptor,
    capsys: pytest.CaptureFixture,
) -> None:
    out_fpath = tmp_path / "pipeline_description.txt"
    pipeline_descriptor.save(out_fpath)

    captured = capsys.readouterr()
    assert "WARNING: file extension" in captured.out
