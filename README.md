# ATIVIDADE PRÁTICA — SISTEMA DE MONITORAMENTO INDUSTRIAL EM PYTHON + MySQL

## **Contexto**

Nesta atividade, os alunos deverão desenvolver um sistema completo que simula um ambiente de **automação industrial**, utilizando a linguagem **Python** para toda a lógica do sistema e o **MySQL Workbench 8.0** para a criação e gerenciamento do banco de dados.

O sistema será responsável por **monitorar máquinas, sensores e leituras de temperatura**, armazenando informações e classificando automaticamente situações de risco.

**Atualmente:**

- Os dados são anotados manualmente
- Não há histórico estruturado
- Não existe análise de qualidade

**A empresa quer um sistema que:**

- Registre dados automaticamente
- Armazene em banco de dados
- Gere histórico
- Permita análise simples

# **Objetivo do Projeto**

Desenvolver um sistema capaz de:

- Cadastrar máquinas, sensores e operadores
- Registrar leituras de sensores (simulação)
- Armazenar dados em banco relacional (MySQL)
- Salvar dados complementares em JSON
- Gerar alertas automáticos com base nas leituras
- Organizar e estruturar informações como um sistema real

# TECNOLOGIAS OBRIGATÓRIAS

- 🐍 Python (toda lógica do sistema)
- 🗄️ MySQL Workbench 8.0 (banco de dados)
- 📁 JSON (armazenamento complementar)
- 🌐 GitHub (versionamento e entrega)

# ESTRUTURA DO BANCO DE DADOS

Todos os grupos deverão criar exatamente **6 tabelas**, conforme definido abaixo:

### 📋 Tabelas obrigatórias:

1. maquinas
2. sensores
3. operadores
4. leituras
5. alertas
6. manutencoes

---

## Relacionamentos obrigatórios:

- sensores → relacionados a maquinas
- leituras → relacionadas a sensores
- alertas → relacionados a leituras
- manutencoes → relacionadas a maquinas e operadores

## Regras obrigatórias:

- Todas as tabelas devem possuir **PRIMARY KEY**
- Deve haver uso de **FOREIGN KEY**
- O banco deve funcionar sem erros

# FUNCIONALIDADES DO SISTEMA

O sistema deverá possuir um menu interativo em Python contendo no mínimo:

---

## Cadastro

- Cadastrar máquinas
- Cadastrar sensores
- Cadastrar operadores

---

## Registro de Dados

- Registrar leituras de sensores (valores simulados)
- Armazenar data e hora automaticamente

---

## Armazenamento

- Salvar dados no banco MySQL
- Salvar dados em arquivo JSON

---

## Consulta

- Listar máquinas
- Listar sensores
- Listar leituras

---

## Análise de Qualidade

O sistema deve classificar automaticamente:

- Até 70°C → NORMAL
- 71°C a 90°C → ALERTA
- Acima de 90°C → CRÍTICO

Deve registrar essas informações na tabela **alertas**

# PENSAMENTO SISTÊMICO (OBRIGATÓRIO)

O sistema deve seguir o fluxo:

Entrada → Processamento → Armazenamento → Saída

Os alunos devem demonstrar entendimento desse fluxo na documentação.

---

# DOCUMENTAÇÃO OBRIGATÓRIA

Cada grupo deverá entregar um documento contendo:

---

## Conteúdo mínimo:

### 1. Introdução

- Contexto do projeto

### 2. Objetivo

- O que o sistema resolve

### 3. Banco de Dados

- Quantidade de tabelas: **6 (obrigatório)**
- Nome e função de cada tabela
- Relacionamentos

### 4. Funcionamento do Sistema

- Explicação do fluxo

### 5. Código

- Explicação das principais funções

### 6. Evidências

- Prints do sistema
- Prints do banco

---

# ENTREGA NO GITHUB (OBRIGATÓRIO)

## O grupo deverá:

- Cada um do grupo deve criar um repositório no GitHub
- Subir todos os arquivos do projeto

---

## 📁 Estrutura obrigatória:

```
/Projeto-Automacao
│── /codigo
│── /banco
│── /dados_json
│── /documentacao
│── README.md
```

---

## Entrega:

- Link do repositório
- Repositório deve estar acessível

---

# TRABALHO EM GRUPO

- A atividade será realizada em grupo
- Todos devem participar do desenvolvimento
- **Todos os integrantes devem entregar individualmente**

## CRITÉRIOS DE AVALIAÇÃO

| Critério | Pontos |
| --- | --- |
| Funcionamento do sistema | 2 |
| Banco de dados (6 tabelas) | 2 |
| Relacionamentos corretos | 2 |
| Integração Python + MySQL | 1 |
| Uso de JSON | 1 |
| Documentação | 1 |
| Organização do projeto | 1 |

# ERROS QUE INVALIDAM

- Não utilizar Python como base do sistema
- Banco com menos ou mais de 6 tabelas
- Falta de relacionamento entre tabelas
- Não utilizar MySQL
- Não entregar no GitHub
- Falta de documentação
