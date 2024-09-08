import os
import subprocess
import json

def parse_pd_file(filepath):
    objects = []

    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('#X obj'):
                parts = line.strip().split()
                if len(parts) >= 5:
                    obj_x = parts[2]  # Coordenada X
                    obj_y = parts[3]  # Coordenada Y
                    obj_type = parts[4]  # Tipo do objeto
                    parameters = ' '.join(parts[5:]).replace(';', '').strip().lower()  # Parâmetros

                    # Se o tipo contém '/', separe e adicione cada subtipo
                    if '/' in obj_type:
                        obj_types = obj_type.split('/')
                        for subtype in obj_types:
                            objects.append({
                                'type': subtype.replace(';', '').lower(),
                                'parameters': parameters,
                                'X': obj_x,
                                'Y': obj_y
                            })
                    else:
                        if obj_type == 'route':
                            route_values = parameters.split()
                            for i, value in enumerate(route_values):
                                objects.append({
                                    'type': obj_type.replace(';', '').lower(),
                                    'parameters': value,
                                    'plug_{}'.format(i): value,
                                    'X': obj_x,
                                    'Y': obj_y
                                })
                        else:
                            objects.append({
                                'type': obj_type.replace(';', '').lower(),
                                'parameters': parameters,
                                'X': obj_x,
                                'Y': obj_y
                            })

    return objects

def index_pd_files(directory):
    index = {}
    metadata_directory = 'projetos/pdSearch/_data'
    consolidated_data = []  # Inicializa como uma lista
    
    # Cria o diretório de metadados se não existir
    if not os.path.exists(metadata_directory):
        os.makedirs(metadata_directory)
    
    for filename in os.listdir(directory):
        if filename.endswith('.pd'):
            filepath = os.path.join(directory, filename)
            objects = parse_pd_file(filepath)
            
            # Salvando JSON individual de cada projeto
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_filepath = os.path.join(metadata_directory, json_filename)
            
            with open(json_filepath, 'w') as json_file:
                json.dump({'filename': filename, 'objects': objects}, json_file, indent=4)
            
            index[filename] = json_filepath
            
            # Adicionando dados diretamente à lista consolidada
            consolidated_data.append({
                'filename': filename,
                'objects': objects
            })
    
    # Salvando o arquivo consolidado
    consolidated_filepath = os.path.join(metadata_directory, 'bd.json')
    with open(consolidated_filepath, 'w') as json_file:
        json.dump(consolidated_data, json_file, indent=4)
    
    return index

# Caminho para o diretório dos arquivos .pd
pd_directory_path = 'projetos/pdSearch/PD'
script_directory_path = 'projetos/pdSearch/scripts'
index = index_pd_files(pd_directory_path)

print(f"Arquivos JSON gerados: {index}")
