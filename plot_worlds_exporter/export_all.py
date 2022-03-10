import json
import anvil
import shutil
import os
from nbt import nbt
import argparse

# METADATA_FILE_NAME = "../data/exported_metadata.json"
# INPUT_WORLD_PATH = "plots/"
# TEMPALTE_WORLD_PATH = "flat_world_template/"
# OUTPUT_PATH = "output/"

REGION_FILE_PATH_TEMPLATE = "region/r.{}.{}.mca"
TEMP_PATH = "tmp/world/"

class Config:
    START_CHUNK_X = 0
    START_CHUNK_Z = 0
    AREA_WIDTH_CHUNKS = 0
    WORLD_PATH = ""

regions_cache = {}

def get_region(basepath, x, z):
    if (x, z) in regions_cache:
        return regions_cache[(x, z)]
    else:
        region = anvil.Region.from_file(os.path.join(basepath, REGION_FILE_PATH_TEMPLATE.format(x, z)))
        regions_cache[(x, z)] = region
        return region

def convert_plot(config, plot_x, plot_z):
    start_x = config.START_CHUNK_X + plot_x * config.AREA_WIDTH_CHUNKS
    start_z = config.START_CHUNK_Z + plot_z * config.AREA_WIDTH_CHUNKS
    end_x = config.START_CHUNK_X + (plot_x + 1) * config.AREA_WIDTH_CHUNKS
    end_z = config.START_CHUNK_Z + (plot_z + 1) * config.AREA_WIDTH_CHUNKS

    export_region = anvil.EmptyRegion(0, 0)

    export_x = (32 - config.AREA_WIDTH_CHUNKS) // 2 + 1
    for x in range(start_x, end_x):
        export_z = (32 - config.AREA_WIDTH_CHUNKS) // 2 + 1
        for z in range(start_z, end_z):
            region_x = x // 32
            region_z = z // 32
            r = get_region(config.WORLD_PATH, region_x, region_z)
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
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--metadata', '-m', type=str, required=True, help='exported metadata file')
    parser.add_argument('--input', '-i', type=str, required=True, help='path to input world')
    parser.add_argument('--template', '-t', type=str, required=True, help='path to template world')
    parser.add_argument('--output', '-o', type=str, required=True, help='output path')
    parser.add_argument('--road-width', '-rw', type=int, required=True, help='width (in chunks) of roads in plots world')
    parser.add_argument('--plot-width', '-pw', type=int, required=True, help='width (in chunks) of plot area in plots world')
    parser.add_argument('--start-x', '-sx', type=int, required=True, help='X coordinate of min chunk of plot area including part of road with plot address (0,0)')
    parser.add_argument('--start-z', '-sz', type=int, required=True, help='X coordinate of min chunk of plot area including part of road with plot address (0,0)')

    args = parser.parse_args()

    config = Config()
    config.START_CHUNK_X = args.start_x
    config.START_CHUNK_Z = args.start_z
    config.AREA_WIDTH_CHUNKS = args.road_width + args.plot_width
    config.WORLD_PATH = args.input

    with open(args.metadata, "r") as metadata_file:
        metadata = json.load(metadata_file)

    for item in metadata:
        plot_id = item["id"]
        plot_list_id = item["plot_list_id"]
        plot_x = int(plot_id.split(".")[1])
        plot_z = int(plot_id.split(".")[2])
        converted_region = convert_plot(config, plot_x, plot_z)

        shutil.rmtree(TEMP_PATH, ignore_errors=True)
        os.makedirs(TEMP_PATH)
        os.mkdir(os.path.join(TEMP_PATH, "region"))
        shutil.copyfile(os.path.join(args.template, "level.dat"), os.path.join(TEMP_PATH, "level.dat"))
        converted_region.save(os.path.join(TEMP_PATH, "region","r.0.0.mca"))

        exported_world_name = "plot_{}_world".format(plot_list_id)
        shutil.make_archive(os.path.join(args.output, exported_world_name), 'zip', "tmp/")

main()
