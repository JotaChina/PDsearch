import os
from bs4 import BeautifulSoup

# Pasta onde os arquivos HTML estão armazenados
pasta_html = 'output_pages/'

def verificar_itens_na_tabela(html_content, itens):
    soup = BeautifulSoup(html_content, 'html.parser')
    tabela = soup.find('table')
    
    if tabela:
        linhas = tabela.find_all('tr')
        for linha in linhas:
            colunas = linha.find_all('td')
            for coluna in colunas:
                texto_coluna = coluna.get_text(strip=True)
                if texto_coluna in itens:
                    return True
    return False

def buscar_itens_em_pastas(itens):
    resultados = []
    for filename in os.listdir(pasta_html):
        if filename.endswith('.html'):
            with open(os.path.join(pasta_html, filename), 'r', encoding='utf-8') as file:
                html_content = file.read()
                if verificar_itens_na_tabela(html_content, itens):
                    resultados.append(filename)
    return resultados

if __name__ == "__main__":
    itens_busca = input("Digite os itens a serem buscados, separados por vírgula: ").split(',')
    itens_busca = [item.strip() for item in itens_busca]
    
    resultados = buscar_itens_em_pastas(itens_busca)
    
    if resultados:
        print("Projetos com os itens especificados:")
        for resultado in resultados:
            print(resultado)
    else:
        print("Nenhum projeto contém os itens especificados.")

