from flask import Flask, request, render_template, jsonify
from pynYNAB.Client import nYnabClientFactory
from pynYNAB.connection import nYnabConnection
from pynYNAB.schema import Transaction
import json
import datetime
import calendar as c

app = Flask(__name__)

@app.route('/')
def calendar():
    return render_template("json.html")

@app.route('/data')
def return_data():
    email = 'YOUR_EMAIL'
    password = 'YOUR_PASSWORD'
    budget_name= 'YOUR_BUDGET_NAME'
    connection = nYnabConnection(email, password)
    connection.init_session()
    client = nYnabClientFactory().create_client(email, password, budget_name, connection)
    client.sync()

    #Get current date,year,month
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    #Create dictionary of current months days
    num_days = c.monthrange(year, month)[1]
    current_month_days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    month_dict = dict((el,0) for el in current_month_days)

    #Set dictionary values as transaction totals
    for i in current_month_days:
        for t in client.budget.transactions:
            if i == t.date:
                month_dict[t.date]+= t.amount

    #Set all values to 2 decimal points
    for key, value in month_dict.items():
        month_dict[key] = float("{0:.2f}".format(value))

    #Create list of dictionaries
    final_data = []

    for key,value in month_dict.items():
        if value<0:
            final_data.append({'title':value,
                       'start':key.strftime('%Y-%m-%d'),
                          'color':'#f08080'})
        elif value>0:
            final_data.append({'title':value,
                       'start':key.strftime('%Y-%m-%d'),
                         'color':'#b4eeb4'})

        else:
            final_data.append({'title':value,
                       'start':key.strftime('%Y-%m-%d'),
                       'color':'white'})


    return jsonify(final_data)

if __name__ == '__main__':
    app.debug = True
    app.run()
