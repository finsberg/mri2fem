from mri2fem import (
    freesurfer,
)

from config import MRI2FEMDATADIR, SUBJECTS_DIR, DATADIR


def extract_ventricles(
    input=MRI2FEMDATADIR / "freesurfer" / "ernie" / "mri" / "wmparc.mgz",
    ventricles_stl=DATADIR / "ernie" / "ventricles.stl",
    include_fourth_and_aqueduct: bool = True,
    num_closing=2,
    V_min=100,
    num_smoothing=1,
    postprocess=True,
):
    matchval = "15" if include_fourth_and_aqueduct else "1"

    assert input.exists(), f"File {input} not found. Please download the data first"

    ventricles_stl.parent.mkdir(exist_ok=True, parents=True)

    if postprocess:
        tmp_mgz = DATADIR / "ernie" / "tmp.mgz"

        freesurfer.run(
            entrypoint="mri_binarize",
            args=[
                "--i",
                "/usr/local/freesurfer/subjects/" + str(input.relative_to(SUBJECTS_DIR)),
                "--ventricles",
                "--o",
                "/usr/local/freesurfer/results/" + str(tmp_mgz.relative_to(DATADIR)),
            ],
            SUBJECTS_DIR=str(SUBJECTS_DIR),
            RESULTS_DIR=str(DATADIR),
        )
        # assert tmp_mgz.exists()

        tmp_ocn_mgz = DATADIR / "ernie" / "tmp-ocn.mgz"

        freesurfer.run(
            entrypoint="mri_volcluster",
            args=[
                "--in",
                "/usr/local/freesurfer/results/" + str(tmp_mgz.relative_to(DATADIR)),
                "--thmin",
                "1",
                "--minsize",
                str(V_min),
                "--ocn",
                "/usr/local/freesurfer/results/" + str(tmp_ocn_mgz.relative_to(DATADIR)),
            ],
            RESULTS_DIR=str(DATADIR),
        )
        # assert tmp_ocn_mgz.exists()

        freesurfer.run(
            entrypoint="mri_binarize",
            args=[
                "--i",
                "/usr/local/freesurfer/results/" + str(tmp_ocn_mgz.relative_to(DATADIR)),
                "--match",
                "1",
                "--o",
                "/usr/local/freesurfer/results/" + str(tmp_mgz.relative_to(DATADIR)),
            ],
            RESULTS_DIR=str(DATADIR),
        )

        freesurfer.run(
            entrypoint="mri_morphology",
            args=[
                "/usr/local/freesurfer/results/" + str(tmp_mgz.relative_to(DATADIR)),
                "close",
                str(num_closing),
                "/usr/local/freesurfer/results/" + str(tmp_mgz.relative_to(DATADIR)),
            ],
            RESULTS_DIR=str(DATADIR),
        )

        freesurfer.run(
            entrypoint="mri_binarize",
            args=[
                "--i",
                "/usr/local/freesurfer/results/" + str(tmp_mgz.relative_to(DATADIR)),
                "--match",
                "1",
                "--surf-smooth",
                str(num_smoothing),
                "--surf",
                "/usr/local/freesurfer/results/" + str(ventricles_stl.relative_to(DATADIR)),
            ],
            RESULTS_DIR=str(DATADIR),
        )

        tmp_mgz.unlink(missing_ok=True)
        tmp_ocn_mgz.unlink(missing_ok=True)

    else:
        freesurfer.run(
            entrypoint="mri_binarize",
            args=[
                "--i",
                "/usr/local/freesurfer/subjects/" + str(input.relative_to(SUBJECTS_DIR)),
                "--match",
                matchval,
                "--surf-smooth",
                str(num_smoothing),
                "--surf",
                "/usr/local/freesurfer/results/" + str(ventricles_stl.relative_to(DATADIR)),
            ],
            SUBJECTS_DIR=str(SUBJECTS_DIR),
            RESULTS_DIR=str(DATADIR),
        )
    assert ventricles_stl.exists()
