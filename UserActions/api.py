
import flask
from flask import request, jsonify

import accounts
import quotes
import buy
import sell
import setbuy
import setsell
import logs

app = flask.Flask(__name__)
app.config["DEBUG"] = True


#Database queries
@app.route('/useraccount', methods=['POST'])
def get_user():
    query_params = request.get_json()
    user_id = query_params["id"]

    result = accounts.find_user_account(user_id)
    return jsonify(result)


@app.route('/userstocks', methods=['POST'])
def get_user_stocks():
    query_params = request.get_json()
    user_id = query_params["id"]

    
    result = accounts.get_user_stocks(user_id)
    # print("The info is --> ", result)
    return jsonify(result)

#Generic functions
@app.route('/ADD', methods=['POST'])
def add_funds_to_account():
    query_params = request.get_json()

    user_id = query_params["id"]
    amount = float(query_params["amount"])

    #update user account with added money
    result = accounts.add_funds(user_id, amount)

    response = {
        "userid": result["id"],
        "balance": result["amount"]
    }

    return jsonify(response)

@app.route('/QUOTE', methods=["POST"])
def quote_stock():
    query_params = request.get_json()
    print(query_params)

    user_id = query_params["id"]
    stock_name = query_params["stock"]

    
    result = quotes.get_quote(user_id, stock_name)
    print("The stock quote result is --> ", result)

    return jsonify(result)

#Buy
@app.route('/BUY', methods=['POST'])
def buy_stock():
    query_params = request.get_json()

    user_id = query_params["id"]
    stock_name = query_params["stock"]
    amount = float(query_params["amount"])
    print("Buy for ", user_id)
    result = buy.start_buy(user_id, stock_name, amount)
    print(jsonify(result))
    return jsonify(result)

@app.route('/COMMIT_BUY', methods=['POST'])
def commit_buy_stock():
    query_params = request.get_json()
    user_id = query_params["id"]
    print("Commiting most recent buy for ", user_id)
    result = buy.commit_buy(user_id)
    print(jsonify(result))
    return jsonify(result)

@app.route('/CANCEL_BUY', methods=['POST'])
def cancel_buy_stock():
    query_params = request.get_json()
    user_id = query_params["id"]
    print("cancelling most recent buy for ", user_id)
    result = buy.cancel_buy(user_id)
    return jsonify(result)

#Sell
@app.route('/SELL', methods=['POST'])
def sell_stock():
    query_params = request.get_json()
    user_id = query_params["id"]
    stock_name = query_params["stock"]
    amount = float(query_params["amount"])
    print("Executing sell for ", user_id, stock_name)
    result = sell.start_sell(user_id, stock_name, amount)
    return jsonify(result)

@app.route('/COMMIT_SELL', methods=['POST'])
def commit_sell_stock():
    query_params = request.get_json()
    user_id = query_params["id"]
    
    result = sell.commit_sell(user_id)
    return jsonify(result)

@app.route('/CANCEL_SELL', methods=['POST'])
def cancel_sell_stock():
    query_params = request.get_json()
    user_id = query_params["id"]
    print("Cancel recent sell  for ", user_id)
    result = sell.cancel_sell(user_id)
    return jsonify(result)

#Set Buy
@app.route('/SET_BUY_AMOUNT', methods=['POST'])
def set_buy_stock():
    query_params = request.get_json()
    user_id = query_params["id"]
    stock_name = query_params["stock"]
    amount = float(query_params["amount"])

    #query for user cash amount
    #if sufficient:
    #   create a log of trans
    #   create reserve account holding allocated funds?
    #   update db with decreased cash amount, trigger amount
    result = setbuy.set_buy_amount(user_id, stock_name, amount)

    return jsonify(result)

@app.route('/SET_BUY_TRIGGER', methods=['POST'])
def set_buy_stock_trigger():
    query_params = request.get_json()
    user_id = query_params["id"]
    stock_name = query_params["stock"]
    amount = float(query_params["amount"])

    #query for quoteserver stock price
    #create and commit a buy action if the stock price <= trigger amount
    result = setbuy.set_buy_trigger(user_id, stock_name, amount)

    return jsonify(result)

@app.route('/CANCEL_SET_BUY', methods=['POST'])
def cancel_set_buy_stock():
    query_params = request.get_json()
    user_id = query_params["id"]
    stock_name = query_params["stock"]

    #query transactions (or user account?) for a set buy amount
    #if exists,
    #   account is reset to the value before the set buy
    #   remove the buy trigger
    #   create a transaction log
    result = setbuy.cancel_set_buy(user_id, stock_name)

    return jsonify(result)

#Set Sell
@app.route('/SET_SELL_AMOUNT', methods=['POST'])
def set_sell_stock_amount():
    query_params = request.get_json()
    user_id = query_params["id"]
    stock_name = query_params["stock"]
    amount = float(query_params["amount"])

    #query for user stock amount
    #if sufficient:
    #   create a log of trans
    #   create reserve account holding allocated stocks?
    #   update db with decreased stock amount, trigger amount
    result = setsell.set_sell_amount(user_id, stock_name, amount)

    return jsonify(result)

@app.route('/SET_SELL_TRIGGER', methods=['POST'])
def set_sell_stock_trigger():
    query_params = request.get_json()
    user_id = query_params["id"]
    stock_name = query_params["stock"]
    amount = float(query_params["amount"])

    #query for quoteserver stock price
    #create and commit a sell action if the stock price >= trigger amount
    result = setsell.set_sell_trigger(user_id, stock_name, amount)

    return jsonify(result)

@app.route('/CANCEL_SET_SELL', methods=['POST'])
def cancel_set_sell_stock():
    query_params = request.get_json()
    user_id = query_params["id"]
    stock_name = query_params["stock"]

    #query transactions (or user account?) for a set sell amount
    #if exists,
    #   account is reset to the value before the set sell
    #   remove the sell trigger
    #   create a transaction log
    result = setsell.cancel_set_sell(user_id, stock_name)

    return jsonify(result)

#Logs
@app.route('/USER_DUMPLOG', methods=['POST'])
def user_dumplog_endpoint():
    query_params = request.get_json()
    user_id = query_params['id']
    output_file = query_params.get('filename')

    result = logs.user_dumplog(user_id, output_file)
    return result

@app.route('/DUMPLOG', methods=['POST'])
def dumplog_endpoint():
    query_params = request.get_json()
    output_file = query_params.get('filename')

    result = logs.dumplog(output_file)
    return result

@app.route('/DISPLAY_SUMMARY', methods=['POST'])
def display_summary_endpoint():
    query_params = request.get_json()
    user_id = query_params["id"]

    result = logs.display_summary(user_id)
    return jsonify(result)


app.run(host="0.0.0.0", port=5000)