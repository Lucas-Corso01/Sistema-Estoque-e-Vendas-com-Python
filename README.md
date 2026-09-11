# 📦 Sistema de Estoque e Vendas

Sistema desenvolvido em **Python** para gerenciamento de produtos, clientes, estoque e vendas, aplicando conceitos de **Estruturas de Dados, Algoritmos e Programação Orientada a Objetos**.

## 👨‍💻 Desenvolvedores

- **Lucas A. C. Castelli**
- **Lucas Ribas**
- **Gabriel T. Bordignon**
- **Rodolpho Simaenski**
- **Mateus Rigon**

## 🛠️ Tecnologias

- **Python 3**
- Arquivos **CSV** para persistência dos dados
- Programação Orientada a Objetos
- Estruturas de dados implementadas manualmente

## 🧠 Estruturas de Dados

O projeto utiliza:

- **Lista Simplesmente Encadeada (LSE)** — armazenamento e manipulação de dados.
- **Lista Duplamente Encadeada (LDE)** — permite percorrer os produtos nos dois sentidos.
- **Fila (FIFO)** — utilizada no gerenciamento das vendas.
- **Pilha (LIFO)** — utilizada para o sistema de desfazer operações.

## 🔎 Algoritmos

- **Insertion Sort** para ordenação dos produtos.
- **Busca Binária** para localizar produtos pelo código.

Antes da busca binária, os produtos são ordenados para garantir o funcionamento correto do algoritmo.

## ⚙️ Funcionalidades

O sistema permite:

- Cadastrar, consultar, atualizar e remover produtos;
- Cadastrar e consultar clientes;
- Controlar o estoque;
- Realizar vendas;
- Calcular automaticamente o valor total das vendas;
- Consultar o histórico de vendas;
- Listar produtos em ordem normal e inversa;
- Ordenar e buscar produtos;
- Desfazer operações;
- Salvar e carregar dados através de arquivos CSV.

## 📁 Organização

```text
Sistema-Estoque-e-Vendas-com-Python/
├── algoritmos/
├── estruturas/
├── models/
├── services/
├── data/
├── main.py
└── README.md
```

## ▶️ Como executar

É necessário ter o **Python 3** instalado.

No terminal, dentro da pasta do projeto:

```bash
python main.py
```

No Windows, também pode ser utilizado:

```bash
py main.py
```

## 💾 Persistência

Os dados do sistema são armazenados na pasta `data/`, utilizando arquivos CSV:

- `clientes.csv`
- `produtos.csv`
- `vendas.csv`

Assim, os dados permanecem salvos mesmo após o encerramento do programa.

## 🎓 Objetivo

O projeto foi desenvolvido com finalidade acadêmica, colocando em prática conceitos de **estruturas de dados, algoritmos, POO, modularização e persistência de dados**.
