import csv
import json
import shutil
import os

INPUT_SCHEMATICS_PATH = "exported_schematics/"
OUTPUT_SCHEMATICS_PATH = "../public/data/models/"
INPUT_PRESENTATIONS_PATH = "downloaded_presentations/"
OUTPUT_PRESENTATIONS_PATH = "../public/data/media/"

OUTPUT_METADATA_FILE = "../public/data/metadata.json"

MEDIA_ID_GENERATOR = 1

with open("metadata_editor.csv") as metadata_file:
    reader = csv.DictReader(metadata_file)

    public_metadata = []
    used_ids = []

    for item in reader:
        simple_id = item["SimpleId"]
        if simple_id in used_ids:
            print("Warning: Ignoring duplicated id {}, row data: {}".format(simple_id, str(item)))
            continue

        if item["Excluded"] == '1':
            print("Warning: Item with id {} excluded".format(simple_id))
            continue

        modelname = "model{}".format(simple_id)

        # Presentations
        presentations = item["Presentations"]
        files = presentations.split(";;")
        pres = []
        for pres_file in files:
            if pres_file.endswith(".pdf"):
                pres_type = "pdf"
                file_ext = "pdf"
            elif pres_file.endswith(".mp4"):
                pres_type = "video"
                file_ext = "mp4"
            else:
                print("Warning: Ignoring invalid presentation {} for id {}".format(pres_file, simple_id))
                continue
            media_file_name = "media_{}_{}.{}".format(pres_type, MEDIA_ID_GENERATOR, file_ext)
            MEDIA_ID_GENERATOR += 1
            shutil.copyfile(
                os.path.join(INPUT_PRESENTATIONS_PATH, pres_file),
                os.path.join(OUTPUT_PRESENTATIONS_PATH, media_file_name))
            pres.append({
                "type": pres_type,
                "src": media_file_name
            })

        meta = {
            "title": "Команда {}".format(simple_id),
            "model": modelname,
            "pres": pres
        }
        public_metadata.append(meta)
        shutil.copyfile(
            os.path.join(INPUT_SCHEMATICS_PATH, item["Schematic"]),
            os.path.join(OUTPUT_SCHEMATICS_PATH, "{}.schem".format(modelname)))


with open(OUTPUT_METADATA_FILE, "w", encoding="utf8") as output_file:
    json.dump(public_metadata, output_file, indent=2, ensure_ascii=False)
