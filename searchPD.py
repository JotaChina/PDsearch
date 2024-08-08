import os
import json
from collections import defaultdict

def load_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data.append(json.load(file))
    return data

def index_instruments(data):
    instrument_projects = defaultdict(lambda: defaultdict(list))
    for project in data:
        filename = project['filename']
        for obj in project['objects']:
            instrument_type = obj['type']
            if instrument_type == 'route':
                # Processa os parâmetros separados para o tipo 'route'
                route_parameters = obj['parameters'].split()
                for param in route_parameters:
                    # Usa o parâmetro como uma chave de instrumento
                    instrument_projects[param][filename].append(obj)
            else:
                # Processa outros tipos de instrumentos
                instrument_projects[instrument_type][filename].append(obj)
    return instrument_projects

def search_instruments(instrument_projects, search_term):
    results = defaultdict(lambda: defaultdict(list))
    search_parts = search_term.split()
    if not search_parts:
        return results

    search_type = search_parts[0]
    search_params = ' '.join(search_parts[1:]).strip()
    print(search_type, search_params)

    for instrument, projects in instrument_projects.items():
        #dac~ or route /myButton
        print(instrument)
        if search_type == instrument or search_params == instrument:
            print(search_params)
            for project, configs in projects.items():
                for config in configs:
                    if search_params in config['parameters']:
                        results[instrument][project].append(config)
    
    return results

def main():
    directory_path = './_metadata' 
    data = load_json_files(directory_path)
    instrument_projects = index_instruments(data)

    search_term = input("Digite o tipo e parâmetros para buscar (ex: route /myButton): ").strip()
    results = search_instruments(instrument_projects, search_term)

    if results:
        print("Instrumentos encontrados:")
        for instrument, projects in results.items():
            print(f"Tipo: {instrument}")
            for project, configs in projects.items():
                print(f"  Projeto: {project}")
                for config in configs:
                    print(f"    {config['type']} X: {config['X']} Y: {config['Y']}")
    else:
        print("Nenhum projeto encontrado com o termo de busca fornecido.")

if __name__ == "__main__":
    main()
