from flask import Flask, jsonify, request, Response
import requests
import csv
import io

app = Flask(__name__)
API_BASE_URL = "https://sidebar.stract.to/api"
HEADERS = {"Authorization": "ProcessoSeletivoStract2025"}

DEV_INFO = {
    "name": "Davi Magalhães Teixeira",
    "email": "daviteixeira077@gmail.com",
    "linkedin": "https://www.linkedin.com/in/davi-magalh%C3%A3es-75b574257/"
}

# Função para fazer requisições à API da Stract
def fetch_data(endpoint, params=None):
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    return None
    
# Rota inicial
@app.route('/')
def home():
    return jsonify(DEV_INFO)

# Gera CSV a partir de dados
def generate_csv(data, headers):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
    return Response(output.getvalue(), mimetype='text/csv')

# Endpoint para listar anúncios por plataforma
@app.route('/<platform>')
def platform_data(platform):
    accounts = fetch_data(f"accounts?platform={platform}")
    if not accounts:
        return jsonify({"error": "Plataforma não encontrada"}), 404
    
    insights = []
    for account in accounts.get("accounts", []):
        fields = fetch_data(f"fields?platform={platform}")
        field_values = ','.join([f["value"] for f in fields.get("fields", [])])
        insights_data = fetch_data(f"insights?platform={platform}&account={account['id']}&token={account['token']}&fields={field_values}")
        
        if insights_data:
            for item in insights_data.get("insights", []):
                item["Platform"] = platform
                item["Account Name"] = account["name"]
                insights.append(item)
    
    if not insights:
        return jsonify({"error": "Nenhum dado encontrado"}), 404
    
    headers = list(insights[0].keys())
    return generate_csv(insights, headers)

# Endpoint de resumo por plataforma
@app.route('/<platform>/resumo')
def platform_summary(platform):
    accounts = fetch_data(f"accounts?platform={platform}")
    if not accounts:
        return jsonify({"error": "Plataforma não encontrada"}), 404
    
    aggregated_data = {}
    for account in accounts.get("accounts", []):
        fields = fetch_data(f"fields?platform={platform}")
        field_values = ','.join([f["value"] for f in fields.get("fields", [])])
        insights_data = fetch_data(f"insights?platform={platform}&account={account['id']}&token={account['token']}&fields={field_values}")
        
        if insights_data:
            for item in insights_data.get("insights", []):
                account_name = account["name"]
                if account_name not in aggregated_data:
                    aggregated_data[account_name] = {"Platform": platform, "Account Name": account_name}
                
                for key, value in item.items():
                    if isinstance(value, (int, float)):
                        aggregated_data[account_name][key] = aggregated_data[account_name].get(key, 0) + value
    
    summary = list(aggregated_data.values())
    if not summary:
        return jsonify({"error": "Nenhum dado encontrado"}), 404
    
    headers = list(summary[0].keys())
    return generate_csv(summary, headers)

# Endpoint geral (todos os anúncios de todas as plataformas)
@app.route('/geral')
def general_data():
    platforms = fetch_data("platforms")
    if not platforms:
        return jsonify({"error": "Não foi possível recuperar plataformas"}), 500
    
    print(platforms)

    insights = []
    for platform in platforms.get("platforms", []):
        insights.extend(platform_data(platform["value"]).data.decode().split('\n')[1:])
    
    if not insights:
        return jsonify({"error": "Nenhum dado encontrado"}), 404
    
    return Response('\n'.join(insights), mimetype='text/csv')

# Endpoint geral de resumo
@app.route('/geral/resumo')
def general_summary():
    platforms = fetch_data("platforms")
    if not platforms:
        return jsonify({"error": "Não foi possível recuperar plataformas"}), 500
    
    summary = []
    for platform in platforms.get("platforms", []):
        summary.extend(platform_summary(platform["value"]).data.decode().split('\n')[1:])
    
    if not summary:
        return jsonify({"error": "Nenhum dado encontrado"}), 404
    
    return Response('\n'.join(summary), mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)
