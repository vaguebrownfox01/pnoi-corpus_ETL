import pandas as pd
import hashlib
import random
import string
import shutil
import uuid
import json
import os
import sys

DATA = "DATA_DUMMY/pnoistor_mmmYYYY"

BREATH_LABELS = [
    # begining vowels
    "aa", "ee", "uu", "oo",

    "ii", "xx", # 1
    "ii", "xx", # 2
    "ii", "xx", # 3
    "ii", "xx", # 4
    "ii", "xx", # 5

    # end vowels
    "aa", "ee", "uu", "oo",
]
# BREATH_LABELS_df: pd.DataFrame
# sub_files_df: pd.DataFrame
SUB_FILE_FORMAT = [
    # META data
    "pnoistor_feb2023-SID-META-HS-comnt.json",

    # LBA before 4 locations
    "pnoistor_feb2023-SID-LBA_before_LU-HS-comnt.wav",
    "pnoistor_feb2023-SID-LBA_before_RU-HS-comnt.wav",
    "pnoistor_feb2023-SID-LBA_before_LL-HS-comnt.wav",
    "pnoistor_feb2023-SID-LBA_before_RL-HS-comnt.wav",

    # LBA after 4 locations
    "pnoistor_feb2023-SID-LBA_after_LU-HS-comnt.wav",
    "pnoistor_feb2023-SID-LBA_after_RU-HS-comnt.wav",
    "pnoistor_feb2023-SID-LBA_after_LL-HS-comnt.wav",
    "pnoistor_feb2023-SID-LBA_after_RL-HS-comnt.wav",

    # VBA before 4 locations
    "pnoistor_feb2023-SID-VBA_before-HS-comnt.wav",
    # VBA after 4 locations
    "pnoistor_feb2023-SID-VBA_after-HS-comnt.wav",

    # PFT before
    "pnoistor_feb2023-SID-PFT_before-HS-comnt.pdf",
    # PFT after
    "pnoistor_feb2023-SID-PFT_after-HS-comnt.pdf",

    # Annotations: LBA, VBA, PFT
    "pnoistor_feb2023-SID-LBA_before_LU-HS-comnt.txt",
    "pnoistor_feb2023-SID-LBA_before_RU-HS-comnt.txt",
    "pnoistor_feb2023-SID-LBA_before_LL-HS-comnt.txt",
    "pnoistor_feb2023-SID-LBA_before_RL-HS-comnt.txt",
    "pnoistor_feb2023-SID-LBA_after_LU-HS-comnt.txt",
    "pnoistor_feb2023-SID-LBA_after_RU-HS-comnt.txt",
    "pnoistor_feb2023-SID-LBA_after_LL-HS-comnt.txt",
    "pnoistor_feb2023-SID-LBA_after_RL-HS-comnt.txt",
    "pnoistor_feb2023-SID-VBA_before-HS-comnt.txt",
    "pnoistor_feb2023-SID-VBA_after-HS-comnt.txt",

    "pnoistor_feb2023-SID-PFT_after-HS-comnt.tsv",
    "pnoistor_feb2023-SID-PFT_before-HS-comnt.tsv",
]
sub_files_df_columns = ["app_code", "sid", "class", "hs", "ext"]

# 
def create_anotes(fpath: str) -> None:

    if ".wav" in fpath:
        return
    if ".pdf" in fpath:
        return

    # fill df with breath labels for nth location
    def inc_df(n: int) -> pd.DataFrame:
        _df = BREATH_LABELS_df.copy()

        _df["start"] += n * 100
        _df["end"] += n * 100
        _bb = [
            {
                "start": _df["start"][0],
                "end": _df["end"][len(_df) - 1],
                "label": f"bb{n + 1}",
            }
        ]
        _bb_df = pd.DataFrame(_bb)

        _df = pd.concat([_df, _bb_df])

        return _df

    # create breath annotations
    if "BA_" in fpath:

        # Voice Breath Audio
        if "VBA_" in fpath:
            BREATH_LABELS_full_df = pd.concat([inc_df(n) for n in range(0, 4)])

            BREATH_LABELS_full_df.to_csv(
                fpath,
                columns=["start", "end", "label"],
                sep="\t",
                index=False,
                header=None,
            )

        # Lung Breath Audio export
        if "LBA_" in fpath:
            _bb = {
                "start": 2.5,
                "end": 39.3,
                "label": "",
            }

            if "LU" in fpath: # left upper
                _bb["label"] = f"bb{1}"

            if "RU" in fpath: # right upper
                _bb["label"] = f"bb{2}"

            if "LL" in fpath: # left lower
                _bb["label"] = f"bb{3}"

            if "RL" in fpath: # right lower
                _bb["label"] = f"bb{4}"

            pd.DataFrame([_bb]).to_csv(
                fpath,
                columns=["start", "end", "label"],
                sep="\t",
                index=False,
                header=None,
            )

    # create PFT annotations
    if "PFT_" in fpath:
        _p = [
            {
                "FVC": 1.1,
                "FEV1": 0.7,
            }
        ]

        pd.DataFrame(_p).to_csv(
            fpath, columns=["FVC", "FEV1"], sep="\t", index=False
        )

# create fake metadata
def create_meta(sid, n):
    return {
        "firebaseId": sid,
        "subjectBiodata": {
            "subjectSectionDone": True,
            "subjectType": "Control" if n % 2 == 0 else "Patient",
            "subjectRemunerationDetails": random.randint(123413, 909023),
            "subjectAge": random.randint(18, 70),
            "subjectRemunerationType": "Bank",
            "subjectName": sid.split("_")[0].capitalize(),
            "subjectWeight": random.randint(30, 150),
            "subjectGender": "Male" if random.randint(0, 6) % 2 == 0 else "Female",
            "subjectHeight": random.randint(130, 200),
            "firebaseId": sid,
        },
        "subjectSurvey": {
            "answeredQs": [],
            "firebaseId": sid,
        },
    }


# create fake subjects
def sub_ids(N, sn=7):

    return [
        "_".join(
            [
                "".join(random.choices(string.ascii_lowercase, k=sn))+"dummy",
                uuid.uuid4().hex[:8],
            ]
        )
        for _ in range(N)
    ]

def file_hash(seed):
    m = hashlib.md5()
    m.update(seed.encode("utf-8"))
    new_uuid = uuid.UUID(m.hexdigest())
    return new_uuid.hex[:4]


def make_sub_files(sid, n):

    subpath = f"{DATA}/{sid}"
    os.mkdir(subpath)

    _file_names_df = sub_files_df.copy()
    _file_names_df["sid"] = sid
    _file_names_df["hs"] = [
        file_hash(r["sid"] + r["class"]) for _, r in _file_names_df.iterrows()
    ]

    sub_files = _file_names_df

    for _, fn in sub_files.iterrows():
        fname = "-".join(fn.to_dict().values())

        if (n % 2 == 0) and ("after" in fname):
            continue

        sid = fn["sid"]
        fpath = f"{subpath}/{fname}"
        open(fpath, "a").close()

        create_anotes(fpath)

        if ".json" in fpath:
            meta = create_meta(sid, n)
            with open(fpath, "w") as m:
                json.dump(meta, m, indent=1)

    return sid


def create_fake_dataset(N):
    return [make_sub_files(sid, n) for n, sid in enumerate(sub_ids(N))]

def prep():
    if os.path.exists(DATA):
        shutil.rmtree(DATA)

    os.makedirs(DATA)

    _sub_files_df = pd.DataFrame([fn.split("-") for fn in SUB_FILE_FORMAT])
    _sub_files_df.columns = sub_files_df_columns

    # Breath Annotation dataframe
    _BREATH_LABELS_df = pd.DataFrame(BREATH_LABELS, columns=["label"])
    _BREATH_LABELS_df["start"] = list(range(0, len(_BREATH_LABELS_df) * 4, 4))
    _BREATH_LABELS_df["start"] += 2.5
    _BREATH_LABELS_df["end"] = _BREATH_LABELS_df["start"] + 4

    return _sub_files_df, _BREATH_LABELS_df

sub_files_df, BREATH_LABELS_df = prep()

if __name__ == "__main__":

    args = sys.argv

    if len(args) < 2:
        print("mention number of subujects")
        exit(-1)

    try:
        subject_ids = create_fake_dataset(int(args[1]))


        print(f"created {len(subject_ids)} subjects", subject_ids)

    except Exception as e:
        print("Error: ", e)
