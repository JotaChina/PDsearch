import os
import subprocess

def run_pd_for_all_files(directory): 
  if not os.path.isdir(directory):
    raise ValueError(f"O diretório {directory} não foi encontrado!") 
    # Comando shell para executar o script 
    script = "projetos/pdSearch/scripts/runPD.sh" 
    try: 
      # Executa o script shell com o diretório como argumento 
      subprocess.run([script, directory], check=True) 
    except subprocess.CalledProcessError as e:
      print(f"Erro ao executar o script: {e}")
    except Exception as e: 
      print(f"Erro inesperado: {e}")

pd_directory_path = 'projetos/pdSearch/PD' 
run_pd_for_all_files(pd_directory_path)
