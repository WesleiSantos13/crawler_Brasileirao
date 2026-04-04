# ⚽ Crawler Brasileirão

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/status-concluído-success)
![License](https://img.shields.io/badge/license-MIT-green)

## 📌 Descrição

Este projeto realiza a **coleta, tratamento e armazenamento de dados** do Campeonato Brasileiro Série A para as temporadas:

- 2023  
- 2024  
- 2025  

A coleta é feita via **web scraping** utilizando:

- `requests`
- `BeautifulSoup`

Fonte dos dados: Wikipedia

---

## 🌐 Fontes de Dados

- https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2025_-_Série_A  
- https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2024_-_Série_A  
- https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2023_-_Série_A  

---

## ⚙️ Tecnologias Utilizadas

- Python 3.x  
- BeautifulSoup (Web Scraping)  
- Requests (HTTP)  
- CSV (Armazenamento de dados)  

---

## 🔄 Processamento dos Dados

O projeto realiza diversas etapas de transformação:

- Tratamento de tabelas com `rowspan` e `colspan`  
- Conversão da tabela de confrontos (formato matriz → relacional)  
- Remoção de colunas irrelevantes (ex: `Ref.`)  
- Padronização entre diferentes anos  
- Inclusão da coluna `Ano`  

---

## 📊 Estrutura dos Dados

### 📁 Participantes

| Campo | Descrição |
|------|----------|
| Equipe | Nome do clube |
| Cidade | Cidade sede |
| Estado | UF |
| Em 2022 | Posição na temporada anterior |
| Estádio (mando) | Estádio utilizado |
| Capacidade | Capacidade do estádio |
| Títulos | Número de títulos |
| Ano | Ano da edição |

---

### 📁 Classificação

| Campo | Descrição |
|------|----------|
| Pos | Posição |
| Equipe | Nome do clube |
| Pts | Pontos |
| J | Jogos |
| V | Vitórias |
| E | Empates |
| D | Derrotas |
| GP | Gols pró |
| GC | Gols contra |
| SG | Saldo de gols |
| Classificação ou descenso | Situação final |
| Ano | Ano |

---

### 📁 Confrontos

| Campo | Descrição |
|------|----------|
| Mandante | Time da casa |
| Placar | Resultado |
| Visitante | Adversário |
| Ano | Ano |

---

### 📁 Artilharia

| Campo | Descrição |
|------|----------|
| Pos. | Posição |
| Jogador | Nome |
| Equipe | Clube |
| Gols | Quantidade de gols |
| Ano | Ano |

---

### 📁 Assistência

| Campo | Descrição |
|------|----------|
| Pos. | Posição |
| Jogador | Nome |
| Equipe | Clube |
| Asst. | Assistências |
| Ano | Ano |

---

### 📁 Hat-tricks

| Campo | Descrição |
|------|----------|
| Jogador | Nome |
| Clube | Time |
| Adversário | Adversário |
| Placar | Resultado |
| Data | Data |
| Ano | Ano |

---

## 🗄️ Arquivos Gerados

```bash
Participantes.csv
Classificacao.csv
Confrontos.csv
Artilharia.csv
Assistencia.csv
Hat_tricks.csv