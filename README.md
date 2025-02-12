# API de Relatórios - Processo Seletivo Stract

## 📌 Sobre o Projeto

Este projeto é um servidor local em **Python + Flask** que consome a API da **Stract** e gera relatórios CSV baseados nos dados de anúncios. Ele atende aos seguintes requisitos:

- ✅ Consulta plataformas disponíveis
- ✅ Obtém contas de cada plataforma
- ✅ Extrai insights dos anúncios
- ✅ Gera relatórios CSV para cada plataforma e um relatório geral
- ✅ Endpoints organizados para consulta e resumo

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**
- **Flask** (para a API)
- **Requests** (para consumir a API externa)
- **CSV e io** (para geração de relatórios)

---

## 🚀 Como Rodar o Projeto

### 1️⃣ Clonar o Repositório

```bash
    git clone https://github.com/seuusuario/stract-api.git
    cd stract-api
```

### 2️⃣ Criar e Ativar um Ambiente Virtual (Opcional, mas Recomendado)

```bash
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows
```

### 3️⃣ Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Rodar a API

```bash
python app.py
```

A API estará disponível em [**http://127.0.0.1:5000/**](http://127.0.0.1:5000/)

---

## 🌐 Endpoints Disponíveis e Exemplos

### 🔹 Dados do Desenvolvedor

**GET /**

```bash
curl -X GET http://127.0.0.1:5000/
```

**Resposta:**

```json
{
  "name": "Davi Magalhães Teixeira",
  "email": "daviteixeira077@gmail.com",
  "linkedin": "https://www.linkedin.com/in/davi-magalh%C3%A3es-75b574257/"
}
```

### 🔹 Relatório de uma plataforma específica

**GET /{plataforma}**

```bash
curl -X GET http://127.0.0.1:5000/meta_ads
```

**Resposta:** CSV com todos os anúncios da plataforma `meta_ads`.

### 🔹 Resumo de uma plataforma

**GET /{plataforma}/resumo**

```bash
curl -X GET http://127.0.0.1:5000/meta_ads/resumo
```

**Resposta:** CSV agregando os dados da plataforma `meta_ads`.

### 🔹 Relatório geral (todas as plataformas)

**GET /geral**

```bash
curl -X GET http://127.0.0.1:5000/geral
```

**Resposta:** CSV com todos os anúncios de todas as plataformas.

### 🔹 Resumo geral (todas as plataformas)

**GET /geral/resumo**

```bash
curl -X GET http://127.0.0.1:5000/geral/resumo
```

**Resposta:** CSV agregando dados de todas as plataformas.

---

## 📌 Observações

- Os relatórios são gerados em tempo real.
- O formato **CSV** permite fácil integração com planilhas e ferramentas analíticas.
- O campo **"Cost per Click"** para o **Google Analytics** é calculado (`spend / clicks`).

---

## 📩 Contato

Caso tenha dúvidas ou sugestões, entre em contato:

- 📧 Email: [**daviteixeira077@gmail.com**](mailto:daviteixeira077@gmail.com)
- 🔗 LinkedIn: [Davi Magalhães Teixeira](https://www.linkedin.com/in/davi-magalh%C3%A3es-75b574257/)
