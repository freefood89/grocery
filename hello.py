from flask import Flask, request, render_template , send_file
import json
import random
import calendar
import datetime
import pymongo

app = Flask(__name__)

stores = json.load(open('timesAds.json'))
storeNames = [store['name'] for store in stores]

@app.route('/')
def hello_world():
    return 'Welcome!'

@app.route('/times')
def store_names():
    return json.dumps(storeNames)

@app.route('/times/<storeName>/<int:page>')
def sensor_data(storeName,page):
    if storeName not in storeNames:
        return ('Store Not Found',404)
    filename = 'times_flyers/'+storeName + '_' + str(page) + '.jpg'
    print(filename)
    try:
        return send_file(filename)
    except:
        return ('Flyer Page Not Found',404)
        

if __name__ == '__main__':
    app.run(host='0.0.0.0')
