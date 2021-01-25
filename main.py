from flask import Flask
import requests,json

app = Flask(__name__)
def save_to_history(currency_to,exchange_rate,amount,result):
    f = open('history.txt', 'a')
    f.write(f"{currency_to},{exchange_rate},{amount},{result}\n")
    f.close()
def what_kurs(from_m,to_m,money):
    response = requests.get(f'https://api.exchangeratesapi.io/latest?base={from_m}')
    response_json = response.json()
    rates = response_json['rates']
    result=round(money*rates[to_m],2)
    save_to_history(to_m,rates[to_m],money,result)
    return result
@app.route('/eur_to_usd/<int:amount>')
def eur_to_usd(amount):
    usd=what_kurs("EUR","USD",amount)
    return f"{usd} USD"
@app.route("/eur_to_gbp/<int:amount>")
def eur_to_gbp(amount):
    usd = what_kurs("EUR", "GBP", amount)
    return f"{usd} GBP"
@app.route("/eur_to_php/<int:amount>")
def eur_to_php(amount):
    usd = what_kurs("EUR", "PHP", amount)
    return f"{usd} PHP"
@app.route("/history")
def history():
    f = open('history.txt')
    history=""
    for line in f:
        history += line+"</br>"
    f.close()
    return history

if __name__=="__main__":
    app.run()
