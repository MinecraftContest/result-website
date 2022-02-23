import shutil
import json

with open('exported_metadata.json') as metadata_file:
    metadata = json.load(metadata_file)

public_metadata = []

for item in metadata:
    modelname = 'model{}'.format(item['plot_list_id'])
    meta = {
        'title': 'Команда {}'.format(item['plot_list_id']),
        'model': modelname
    }
    public_metadata.append(meta)
    shutil.copyfile('exported_schematics/{}'.format(item['schematic_name']), '../public/data/models/{}.schem'.format(modelname))

with open('../public/data/metadata.json', 'w', encoding='utf8') as output_file:
    json.dump(public_metadata, output_file, indent=2, ensure_ascii=False)
