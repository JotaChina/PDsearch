import os
import json
from collections import defaultdict

def load_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                file_data = json.load(f)
                if isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    print(f"Formato inesperado no arquivo JSON: {filename}")
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

def generate_html_for_project(project, output_dir, svg_file_path):
    """
    Gera um HTML para um projeto, opcionalmente incluindo um conteúdo SVG.
    
    Parameters:
        project (dict): Um dicionário representando um projeto, contendo chaves 'filename' e 'objects'.
        output_dir (str): Diretório de saída para o HTML gerado.
        svg_file_path (str): Caminho para o arquivo SVG associado ao projeto.
    """
    # Verifica se project é um dicionário
    if not isinstance(project, dict):
        print("O parâmetro 'project' deve ser um dicionário.")
        return
    
    # Obtém o nome do arquivo
    filename = project.get('filename')
    if filename is None:
        print("O dicionário 'project' deve conter a chave 'filename'.")
        return

    # Obtém a lista de objetos
    configs = project.get('objects', [])
    
    # Define o caminho para o arquivo SVG
    svg_filename = filename[0] + '.svg'
    svg_path = os.path.join(svg_file_path, svg_filename)
    
    # Lê o conteúdo do arquivo SVG se fornecido
    svg_content = ""
    if svg_file_path and os.path.isfile(svg_path):
        print(f"Lendo SVG de {svg_path}")
        try:
            with open(svg_path, 'r') as svg_file:
                svg_content = svg_file.read()
        except Exception as e:
            print(f"Erro ao ler o arquivo SVG: {e}")

    # Cria o HTML
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
            .svg-container {{ text-align: center; margin-top: 20px; }}
            svg {{ display: block; margin: 0 auto; }}
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
        parameters = config.get('parameters', '-')
        project_html += f"""
            <tr>
                <td>{config['type']}</td>
                <td>{config.get('X', '-')}</td>
                <td>{config.get('Y', '-')}</td>
                <td>{parameters}</td>
            </tr>
        """
    
    project_html += """
            </tbody>
        </table>
    """
    name = f'../PD/SVG/{filename[0]}.svg'
    print(name)
    if svg_content:
        project_html += f"""
        <div class="svg-container">
        <img src="{ name }" alt="Projeto {filename}">
        </div>
        """
    
    project_html += """
    </body>
    </html>
    """
    
    output_file = os.path.join(output_dir, f"{filename[0]}.html")
    try:
        with open(output_file, 'w') as file:
            file.write(project_html)
    except Exception as e:
        print(f"Erro ao escrever o arquivo HTML: {e}")

def main():
    directory_path = 'projetos/pdSearch/_data'
    output_dir = 'projetos/pdSearch/output_pages'
    svg_file_path = 'projetos/pdSearch/PD/SVG'
    os.makedirs(output_dir, exist_ok=True)
    
    data = load_json_files(directory_path)
    
    for project in data:
        generate_html_for_project(project, output_dir, svg_file_path)
    
    print(f"Páginas HTML geradas no diretório '{output_dir}'.")

if __name__ == "__main__":
    main()
