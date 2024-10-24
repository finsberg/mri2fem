import logging

from mri2fem import download_data

from config import MRI2FEMDATADIR, DATADIR


def main():
    logging.basicConfig(level=logging.DEBUG)
    download_data.download_mri2fem_dataset(MRI2FEMDATADIR.with_suffix(".tar.gz"))
    download_data.download_extra_data(DATADIR.with_suffix(".tar.gz"))


if __name__ == "__main__":
    raise SystemExit(main())
