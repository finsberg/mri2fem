from mri2fem import download_data
from config import MRI2FEMDATADIR


def main():
    download_data.main(MRI2FEMDATADIR)


if __name__ == "__main__":
    raise SystemExit(main())
