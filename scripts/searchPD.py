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

def generate_html_for_project(project, output_dir):
    filename = project['filename']
    configs = project['objects']
    
    project_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{filename}</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ width: 100%; border-collapse: collapse; }}
            table, th, td {{ border: 1px solid black; }}
            th, td {{ padding: 8px; text-align: left; }}
        </style>
    </head>
    <body>
        <h1>Projeto: {filename}</h1>
        <table>
            <thead>
                <tr>
                    <th>Tipo</th>
                    <th>X</th>
                    <th>Y</th>
                    <th>Parâmetros</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for config in configs:
        parameters = config.get('parameters', 'N/A')
        project_html += f"""
            <tr>
                <td>{config['type']}</td>
                <td>{config.get('X', 'N/A')}</td>
                <td>{config.get('Y', 'N/A')}</td>
                <td>{parameters}</td>
            </tr>
        """
    
    project_html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    output_file = os.path.join(output_dir, f"{filename[0]}.html")
    with open(output_file, 'w') as file:
        file.write(project_html)

def main():
    directory_path = './_data'
    output_dir = './output_pages'
    os.makedirs(output_dir, exist_ok=True)
    
    data = load_json_files(directory_path)
    
    for project in data:
        generate_html_for_project(project, output_dir)
    
    print(f"Páginas HTML geradas no diretório '{output_dir}'.")

if __name__ == "__main__":
    main()
