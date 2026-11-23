"""Real storage regression for extensionless attachment filename boundaries."""

from types import SimpleNamespace

import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from horilla.models import upload_path


@pytest.mark.parametrize("filename", ["a" * 99, "a" * 100, "report", "report.pdf"])
def test_upload_path_fits_filefield_and_preserves_content(filename, tmp_path):
    instance = SimpleNamespace(
        _meta=SimpleNamespace(app_label="leave", model_name="leaveallocationrequest"),
        attachment=SimpleNamespace(name=filename),
    )
    storage = FileSystemStorage(location=tmp_path)
    stored = storage.save(upload_path(instance, filename), ContentFile(b"synthetic attachment"), max_length=100)
    assert len(stored) <= 100
    assert stored.startswith("leave/leaveallocationrequest/attachment/")
    if filename.endswith(".pdf"):
        assert stored.endswith(".pdf")
    else:
        assert "." not in stored.rsplit("/", 1)[-1]
    with storage.open(stored, "rb") as content:
        assert content.read() == b"synthetic attachment"
