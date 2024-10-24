from pathlib import Path
import logging
import tarfile

import requests
from tqdm import tqdm

here = Path(__file__).absolute().parent
logger = logging.getLogger(__name__)


def download(path, link, desc=None, params=None):
    if desc is None:
        desc = f"Download data to {path}"
    if params is None:
        params = {}

    response = requests.get(link, params, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True, desc=desc)

    with open(path, "wb") as handle:
        for data in response.iter_content(chunk_size=1000 * 1024):
            progress_bar.update(len(data))
            handle.write(data)
    progress_bar.close()

    folder = path.parent
    logger.info("Extracting %s to %s", path, folder)
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(folder)
    path.unlink()


def add_arguments(parser):
    parser.add_argument(
        "dataset", help="Dataset to download", choices=["mri2fem-dataset", "extra-data"]
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("dataset.tar.gz"),
        help="Output path of the downloaded dataset",
    )


def download_extra_data(output: Path = Path("data.tar.gz")) -> None:
    link = "https://drive.usercontent.google.com/download?export=download"
    params = {"id": "1dnfaOSf3TAejGf5Bks2vU4Rwgt6_ibhl", "confirm": "t"}
    logger.info("Downloading extra data to %s", output)
    download(output, link, params=params)


def download_mri2fem_dataset(output: Path = Path("mri2fem-dataset.tar.gz")) -> None:
    link = " https://zenodo.org/record/4899120/files/mri2fem-dataset.tar.gz?download=1"
    logger.info("Downloading MRI2FEM dataset to %s", output)
    download(output, link)


def main(output: Path, dataset: str) -> None:
    if dataset == "mri2fem-dataset":
        download_mri2fem_dataset(output)
    elif dataset == "extra-data":
        download_extra_data(output)
    else:
        raise ValueError(f"Unknown dataset: {dataset}")
