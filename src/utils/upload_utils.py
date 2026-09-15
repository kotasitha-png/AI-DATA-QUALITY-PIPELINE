from pathlib import Path
from typing import BinaryIO


def save_uploaded_file(
    uploaded_file: BinaryIO,
    filename: str,
) -> str:
    """
    Persist a Streamlit-uploaded file locally so
    Spark can read it using a filesystem path.
    """

    upload_dir = Path(
        "data/uploads"
    )

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_name = Path(
        filename
    ).name

    destination = (
        upload_dir
        / safe_name
    )

    with destination.open(
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return str(destination)