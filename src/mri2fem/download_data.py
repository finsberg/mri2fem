from pathlib import Path
import logging
import tarfile

import requests
from tqdm import tqdm

here = Path(__file__).absolute().parent


def download(path, link, desc=None):
    if desc is None:
        desc = f"Download data to {path}"

    response = requests.get(link, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True, desc=desc)

    with open(path, "wb") as handle:
        for data in response.iter_content(chunk_size=1000 * 1024):
            progress_bar.update(len(data))
            handle.write(data)
    progress_bar.close()


def add_arguments(parser):
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("mri2fem-dataset.tar.gz"),
        help="Output path of the downloaded dataset",
    )


def main(output: Path = Path("mri2fem-dataset.tar.gz")) -> None:
    logger = logging.getLogger(__name__)
    path = Path(output).resolve().with_suffix(".tar.gz")

    link = " https://zenodo.org/record/4899120/files/mri2fem-dataset.tar.gz?download=1"

    logger.info("Downloading MRI2FEM dataset to %s", path)
    download(path=path, link=link)

    folder = path.parent
    logger.info("Extracting %s to %s", path, folder)
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(folder)
    path.unlink()
