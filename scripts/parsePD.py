import os
import json

def parse_pd_file(filepath):
    objects = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('#X obj'):
                objects.append({'type': f'{file}'.lower()})
                # Exemplo de linha: #X obj 50 50 osc~ 440;
                parts = line.strip().split()
                if len(parts) >= 5:
                    obj_x = parts[2] # 50
                    obj_y = parts[3] # 50
                    obj_type = parts[4]  # ex: osc~
                    parameters = ' '.join(parts[5:]).replace(';', '').strip().lower() # 440

                    if '/' in obj_type:
                        obj_types = obj_type.split('/')
                        for subtype in obj_types:
                            objects.append({
                                'type': subtype.replace(';', '').lower(),
                                'parameters': parameters.lower(),
                                'X': obj_x,
                                'Y': obj_y
                            })
                    else:
                        if obj_type == 'route':
                            # Para objetos do tipo 'route', processamos os valores após o tipo
                            route_values = parameters.split()
                            for i, value in enumerate(route_values):
                                objects.append({
                                    'type': obj_type.replace(';', '').lower(),
                                    'parameters': value.lower(),
                                    'plug_{}'.format(i): value,
                                    'X': obj_x,
                                    'Y': obj_y
                                })
                        else:
                            objects.append({
                                'type': obj_type.replace(';', '').lower(),
                                'parameters': parameters.lower(),
                                'X': obj_x,
                                'Y': obj_y
                            })
    return objects

def index_pd_files(directory):
    index = {}
    for filename in os.listdir(directory):
        if filename.endswith('.pd'):
            filepath = os.path.join(directory, filename)
            objects = parse_pd_file(filepath)
            #salvando json
            json_filename = os.path.splitext('../assets/data/'+filename)[0] + '.json'
            json_filepath = os.path.join(directory, json_filename)
            
            with open(json_filepath, 'w') as json_file:
                json.dump({'filename': filename, 'objects': objects}, json_file, indent=4)
            
            index[filename] = json_filepath
    return index

directory_path = './PD'
index = index_pd_files(directory_path)

print(f"Arquivos JSON gerados: {index}")
