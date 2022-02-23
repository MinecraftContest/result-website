import re
import os
import json

SCHEMATICS_DIR_NAME = "exported_schematics"
PLOT_LIST_FILE_NAME = "plots_list.txt"
OUTPUT_FILE_NAME = "exported_metadata.json"

# [1]  plots;0;0 - user2
PLOT_LIST_ITEM_FORMAT = r".*\[(\d+)\]\s*([^;]+)\s*;(-?\d+);(-?\d+)\s*-\s*(\S+)"
# 0;0,plots,6e7d9aa0-0da2-390c-ab6a-377df9d77518.schem
PLOT_SCHEMATIC_NAME_FORMAT = r"(-?\d+);(-?\d+),([^,]+),([^\.]*).schem"

def create_id(plot_world, plot_x, plot_z):
    return "{}.{}.{}".format(plot_world, plot_x, plot_z)

items = {}

# parse plots list
with open(PLOT_LIST_FILE_NAME, 'r') as plots_list_file:
    for line in plots_list_file:
        match = re.match(PLOT_LIST_ITEM_FORMAT, line)
        if match is not None:
            values = match.groups()
            plot_list_id = values[0]
            plot_id = create_id(values[1], values[2], values[3])  # world, plot_x, plot_z
            plot_owner = values[4]
            print(plot_id)
            items[plot_id] = {
                "id": plot_id,
                "plot_list_id": plot_list_id,
                "plot_owner": plot_owner
            }
        else:
            print("Not matched list item {}".format(line))


# scan plots schematics
for schematic in os.listdir(SCHEMATICS_DIR_NAME):
    filename = os.fsdecode(schematic)
    match = re.match(PLOT_SCHEMATIC_NAME_FORMAT, filename)
    if match is not None:
        values = match.groups()
        plot_id = create_id(values[2], values[0], values[1])  # world, plot_x, plot_z
        schematic_uuid = values[3]
        if plot_id not in items:
            print('Unknown schematic with name: {}'.format(filename))
        else:
            item = items[plot_id]
            item['schematic_uuid'] = schematic_uuid
            item['schematic_name'] = filename

    else:
        print("Not matched schematic {}".format(filename))

with open(OUTPUT_FILE_NAME, 'w') as output_file:
    json.dump(list(items.values()), output_file, indent=2)
