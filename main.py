import requests
import sqlite3
from flask import Flask, render_template, g

app = Flask(__name__, template_folder="template")
DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        db = g._database = conn
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def save_to_history(currency_to, exchange_rate, amount, result):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
                insert into exchange_history ('currency_to', exchange_rate, amount,result)
                    values (?, ?, ?, ?)
            """, (currency_to, exchange_rate, amount, result))
    conn.commit()


@app.route('/history/currency/<to_currency>/')
def history_currency(to_currency):
    connection = get_db()
    cursor = connection.cursor()
    resp = cursor.execute("""
                select currency_to, exchange_rate,amount,result
                from exchange_history
                where currency_to = ?
            """, (to_currency, ))
    return render_template('history.html', full_history=resp.fetchall(), static=1)


@app.route('/history/amount_gte/<number>')
def amount_gte(number):
    connection = get_db()
    cursor = connection.cursor()
    resp = cursor.execute("""
                select currency_to, exchange_rate,amount,result
                from exchange_history
                where amount >= ?
            """, (number, ))
    return render_template('history.html', full_history=resp.fetchall(), static=1)


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
def get_history():
    connection = get_db()
    cursor = connection.cursor()
    resp = cursor.execute("""
                    select currency_to, exchange_rate,amount,result
                    from exchange_history
                    where 1
                """)
    return render_template('history.html', full_history=resp.fetchall(), static=1)


@app.route("/history/statistic/")
def statistic():
    connection = get_db()
    cursor = connection.cursor()
    resp = cursor.execute("""
                  select currency_to,sum(result) as sum_result, count(currency_to) as count_res
                    from exchange_history  GROUP BY currency_to;
                """)
    #return str(resp.fetchall())
    return render_template('history.html', full_history=resp.fetchall(), static=0)


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == "__main__":
    #init_db()
    app.run()
