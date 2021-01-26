import requests
from flask import Flask, render_template

app = Flask(__name__, template_folder = "template")

def save_to_history(currency_to, exchange_rate, amount, result):
    with open('history.txt', 'a+') as f:
        f.write(f"{currency_to}, {exchange_rate}, {amount}, {result}\n")

def convert_amount(from_m, to_m, money):
    response = requests.get(f'https://api.exchangeratesapi.io/latest?base={from_m}')
    response_json = response.json()
    rates = response_json['rates']
    result = round(money * rates[to_m], 2)
    save_to_history(to_m, rates[to_m], money, result)
    return result

@app.route('/eur_to_usd/<int:amount>')
def eur_to_usd(amount):
    usd = convert_amount("EUR", "USD", amount)
    return f"{usd} USD"

@app.route("/eur_to_gbp/<int:amount>")
def eur_to_gbp(amount):
    usd = convert_amount("EUR", "GBP", amount)
    return f"{usd} GBP"

@app.route("/eur_to_php/<int:amount>")
def eur_to_php(amount):
    usd = convert_amount("EUR", "PHP", amount)
    return f"{usd} PHP"

@app.route("/history")
def history():
    with open('history.txt', 'r') as f:
        response = f.read().splitlines()
    return render_template('history.html', full_history=response)

if __name__ == "__main__":
    app.run()
