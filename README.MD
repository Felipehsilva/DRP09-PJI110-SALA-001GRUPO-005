# 💈 Sistema de Agendamento - Barbearia

Este projeto é uma plataforma web para gestão de agendamentos de serviços de barbearia, desenvolvido como parte do **Projeto Integrador I**. [cite_start]O software permite que usuários se cadastrem e reservem horários, integrando validações automáticas via APIs externas e fornecendo dados estruturados para integração com outros sistemas. [cite: 1, 9]

## 🚀 Tecnologias Utilizadas

* [cite_start]**Framework Web:** Flask (Python). [cite: 14]
* [cite_start]**Banco de Dados:** MySQL hospedado em nuvem (Aiven). [cite: 14]
* [cite_start]**ORM:** Flask-SQLAlchemy para mapeamento objeto-relacional. [cite: 14]
* [cite_start]**Front-end:** HTML5, CSS3 (Bootstrap 5) e JavaScript. [cite: 14]
* **Consumo de API:** Biblioteca `requests` para integração com serviços externos.

---

## 🛠️ Requisitos Atendidos

### 1. Uso e Fornecimento de API (Requisito Principal)
O sistema opera nas duas frentes de integração exigidas:
* **Uso (Consumo):** Integração com a **BrasilAPI**. O sistema intercepta o agendamento e consulta se a data escolhida é um feriado nacional. Caso positivo, o agendamento é bloqueado por regra de negócio.
* Além disso, a API dos Correios é utilizada na etapa de cadastro para a busca automática de endereços.
* **Fornecimento:** O software disponibiliza endpoints REST que entregam dados em formato JSON:
    * `/api/agendamentos`: Retorna a lista completa de horários marcados.
    * `/api/usuarios`: Retorna a lista de usuários cadastrados (com filtros de segurança).

### 2. Acessibilidade
Implementação de recursos para garantir a inclusão digital:
* **Controle de Fonte:** Funções JavaScript para aumentar ou diminuir o tamanho do texto dinamicamente.
* **Síntese de Voz:** Recurso de leitura de frases utilizando a API de voz do navegador ao interagir com elementos da página.

### 3. Banco de Dados e Nuvem
[cite_start]Utilização de banco de dados **MySQL** configurado em ambiente de nuvem (SaaS), garantindo que a aplicação seja escalável e os dados persistentes fora do ambiente local. [cite: 14]

### 4. Controle de Versão
[cite_start]O projeto utiliza **Git** para controle de versão, com o histórico de commits e organização de pastas seguindo as boas práticas de desenvolvimento. [cite: 15]

---

## 📦 Como Instalar e Rodar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Felipehsilva/DRP09-PJI110-SALA-001GRUPO-005](https://github.com/Felipehsilva/DRP09-PJI110-SALA-001GRUPO-005)
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    python webapp.py
    ```

4.  **Acesse no navegador:**
    `http://127.0.0.1:5000`

---

## 🗺️ Endpoints da API (Fornecimento)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/agendamentos` | Lista todos os agendamentos registrados no banco em JSON |
| `GET` | `/api/usuarios` | Lista os usuários cadastrados em JSON |

---
