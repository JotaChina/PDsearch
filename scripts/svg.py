import os
import subprocess

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
                subprocess.run(['inkscape', ps_filepath, '--export-filename=' + svg_filepath, '--export-plain-svg', '--export-overwrite', '--export-area-page'])
                print(f"Arquivo convertido: {svg_filepath}")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao converter {ps_filepath}: {e}")

ps_directory_path = 'projetos/pdSearch/PD/postscript'
svg_directory_path = 'projetos/pdSearch/PD/SVG'
convert_ps_to_svg(ps_directory_path, svg_directory_path)
