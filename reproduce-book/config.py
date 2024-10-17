import logging
from pathlib import Path

here = Path(__file__).absolute().parent
MRI2FEMDATADIR = here / ".." / "mri2fem-dataset"
SUBJECTS_DIR = (MRI2FEMDATADIR / "freesurfer").absolute()
DICOMDIR = (MRI2FEMDATADIR / "dicom").absolute()
DATADIR = (here / ".." / "data").absolute()


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("mri2fem").setLevel(logging.DEBUG)
