import json
# import os
# import errno
import csv

MAPPING = {
    "SimpleId" : {
        "pos": 0,
        "json_key": "plot_list_id"
    },
    "OnlinePlotId" : {
        "pos": 1,
        "json_key": "id"
    },
    "OnlinePlotOwner" : {
        "pos": 2,
        "json_key": "plot_owner"
    },
    "Schematic": {
        "pos": 3,
        "json_key": "schematic_name"
    },
    "Presentations": {
        "pos": 4
    },
    "Excluded": {
        "pos": 5
    },
}

with open('exported_metadata.json') as metadata_file:
    metadata = json.load(metadata_file)

# flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

with open('metadata_editor.csv', 'x') as output_file:
    writer = csv.writer(output_file)

    # Header
    header = [""] * len(MAPPING)
    for column in MAPPING:
        info = MAPPING[column]
        header[info["pos"]] = column
    writer.writerow(header)

    # Rows
    for item in metadata:
        row = [""] * len(MAPPING)
        for column in MAPPING:
            info = MAPPING[column]
            if "json_key" in info:
                row[info["pos"]] = item[info["json_key"]]
        writer.writerow(row)
