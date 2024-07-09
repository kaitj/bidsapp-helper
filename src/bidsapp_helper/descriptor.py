"""Creation of app / pipeline descriptor."""

import json
import pathlib as pl
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BidsAppDescriptor:
    """App / pipeline descriptor representation."""

    app_name: str
    bids_version: str = "1.9.0"
    dataset_type: str = "derivative"
    app_version: str = "0.1.0"
    repo_url: str | None = None
    author: str | None = None
    author_email: str | None = None
    descriptor: dict[str, Any] = field(init=False)

    def __post_init__(self):
        self._validate_dataset_type()
        self.descriptor = self._generate_descriptor()

    def _validate_dataset_type(self) -> None:
        valid_types = {"raw", "derivative"}
        if self.dataset_type not in valid_types:
            raise ValueError(f"Invalid dataset type - must be one of {valid_types}")

    def _generate_descriptor(self) -> dict[str, Any]:
        return {
            "Name": self.app_name,
            "BIDSVersion": self.bids_version,
            "DatasetType": self.dataset_type,
            "GeneratedBy": {
                "Name": self.app_name,
                "Version": self.app_version,
                "CodeURL": self.repo_url,
                "Author": self.author,
                "AuthorEmail": self.author_email,
            },
        }

    def save(self, fpath: pl.Path | str) -> None:
        """Method to save descriptor object as json."""
        if not (fpath := pl.Path(fpath)).suffix == ".json":
            print("WARNING: file extension is not '.json'.")

        fpath.parent.mkdir(parents=True, exist_ok=True)
        with open(fpath, "w") as out_file:
            json.dump(self.descriptor, out_file, indent=4)
