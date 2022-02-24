import json
import anvil
import shutil
import os
from nbt import nbt

METADATA_FILE_NAME = "../data/exported_metadata.json"
INPUT_WORLD_PATH = "plots/"
REGION_FILE_PATH_TEMPLATE = INPUT_WORLD_PATH + "region/r.{}.{}.mca"
TEMPALTE_WORLD_PATH = "flat_world_template/"
TEMP_PATH = "tmp/world/"
OUTPUT_PATH = "output/"

ROAD_WIDTH = 16
PLOT_WIDTH = 272
ROAD_WIDTH_CHUNKS = 1
PLOT_WIDTH_CHUNKS = 17
AREA_WIDTH_CHUNKS = PLOT_WIDTH_CHUNKS + ROAD_WIDTH_CHUNKS
START_X = -1
START_Z = -288
START_CHUNK_X = -18
START_CHUNK_Z = -18

regions_cache = {}

def get_region(x, z):
    if (x, z) in regions_cache:
        return regions_cache[(x, z)]
    else:
        region = anvil.Region.from_file(REGION_FILE_PATH_TEMPLATE.format(x, z))
        regions_cache[(x, z)] = region
        return region

def convert_plot(plot_x, plot_z):
    start_x = START_CHUNK_X + plot_x * AREA_WIDTH_CHUNKS
    start_z = START_CHUNK_Z + plot_z * AREA_WIDTH_CHUNKS
    end_x = START_CHUNK_X + (plot_x + 1) * AREA_WIDTH_CHUNKS
    end_z = START_CHUNK_Z + (plot_z + 1) * AREA_WIDTH_CHUNKS

    export_region = anvil.EmptyRegion(0, 0)

    export_x = (32 - AREA_WIDTH_CHUNKS) // 2 + 1
    for x in range(start_x, end_x):
        export_z = (32 - AREA_WIDTH_CHUNKS) // 2 + 1
        for z in range(start_z, end_z):
            region_x = x // 32
            region_z = z // 32
            r = get_region(region_x, region_z)
            data = r.chunk_data(x, z)

            # replace chunk position
            data['Level']['xPos'] = nbt.TAG_Int(export_x)
            data['Level']['zPos'] = nbt.TAG_Int(export_z)

            # translate entities positions
            for entity in data['Level']['TileEntities'].tags:
                src_x = entity['x'].value
                src_z = entity['z'].value
                entity['x'] = nbt.TAG_Int(src_x + (export_x - x) * 16)
                entity['z'] = nbt.TAG_Int(src_z + (export_z - z) * 16)

            export_region.add_raw_chunk(export_x, export_z, data)

            export_z += 1
        export_x += 1
    return export_region

def main():
    with open(METADATA_FILE_NAME, "r") as metadata_file:
        metadata = json.load(metadata_file)

    for item in metadata:
        plot_id = item["id"]
        plot_x = int(plot_id.split(".")[1])
        plot_z = int(plot_id.split(".")[2])
        converted_region = convert_plot(plot_x, plot_z)

        shutil.rmtree(TEMP_PATH, ignore_errors=True)
        os.makedirs(TEMP_PATH)
        os.mkdir(os.path.join(TEMP_PATH, "region"))
        shutil.copyfile(os.path.join(TEMPALTE_WORLD_PATH, "level.dat"), os.path.join(TEMP_PATH, "level.dat"))
        converted_region.save(os.path.join(TEMP_PATH, "region","r.0.0.mca"))

        exported_world_name = "plot_{}_{}_world".format(plot_x, plot_z)
        shutil.make_archive(os.path.join(OUTPUT_PATH, exported_world_name), 'zip', "tmp/")

main()
