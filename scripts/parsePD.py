import os
import subprocess
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
    metadata_directory = './_data'
    
    # Cria o diretório de metadados se não existir
    if not os.path.exists(metadata_directory):
        os.makedirs(metadata_directory)
    
    for filename in os.listdir(directory):
        if filename.endswith('.pd'):
            filepath = os.path.join(directory, filename)
            objects = parse_pd_file(filepath)
            
            # Salvando JSON
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_filepath = os.path.join(metadata_directory, json_filename)
            
            with open(json_filepath, 'w') as json_file:
                json.dump({'filename': filename, 'objects': objects}, json_file, indent=4)
            
            index[filename] = json_filepath
    
    return index

def convert_ps_to_svg(ps_directory, svg_directory):
    # Cria o diretório SVG se não existir
    if not os.path.exists(svg_directory):
        os.makedirs(svg_directory)
    
    for filename in os.listdir(ps_directory):
        if filename.endswith('.ps'):
            ps_filepath = os.path.join(ps_directory, filename)
            svg_filename = os.path.splitext(filename)[0] + '.svg'
            svg_filepath = os.path.join(svg_directory, svg_filename)
            
            # Executa o comando Inkscape para converter .ps para .svg
            try:
                subprocess.run(['inkscape', ps_filepath, '--export-filename=' + svg_filepath])
                print(f"Arquivo convertido: {svg_filepath}")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao converter {ps_filepath}: {e}")

# Caminho para o diretório dos arquivos .pd
pd_directory_path = './PD'
index = index_pd_files(pd_directory_path)

# Caminho para os diretórios dos arquivos .ps e .svg
ps_directory_path = './PD/postscript'
svg_directory_path = './PD/SVG'
convert_ps_to_svg(ps_directory_path, svg_directory_path)

print(f"Arquivos JSON gerados: {index}")
