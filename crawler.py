import requests
from bs4 import BeautifulSoup
import csv

url = "https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2025_-_Série_A"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "lxml")

tables = soup.find_all("table", class_="wikitable")
print(f"Tabelas encontradas: {len(tables)}")

# índices das tabelas
indices = [1, 3, 4, 6, 7, 8]

# Busca
for i in indices:

    table = tables[i]

    nome_arquivo = f"tabela_{i}.csv"

    with open(nome_arquivo, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for row in table.find_all("tr"):
            cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
            if cols:
                writer.writerow(cols) 

    print(f"Arquivo criado: {nome_arquivo}")


print("Todas as tabelas foram exportadas!")