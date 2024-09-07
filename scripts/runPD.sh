#!/bin/bash

# Diretório onde os arquivos .pd estão localizados
DIRECTORY="$1"

# Verifica se o diretório foi especificado
if [ -z "$DIRECTORY" ]; then
  echo "Uso: $0 <diretório>"
  exit 1
fi

# Verifica se o diretório existe
if [ ! -d "$DIRECTORY" ]; then
  echo "Erro: Diretório $DIRECTORY não encontrado!"
  exit 1
fi

# Executa o comando pd para cada arquivo .pd no diretório
for pd_file in "$DIRECTORY"/*.pd; do
  if [ -f "$pd_file" ]; then
    echo "Processando $pd_file"
    pd "$pd_file"
  fi
done
