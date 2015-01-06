from flask import Flask, request, render_template , send_file
import json
import random
import calendar
import datetime
import pymongo
import htmlParser
import json

app = Flask(__name__)

# stores = json.load(open('timesAds.json'))
# storeNames = [store['name'] for store in stores]
stores = ['nijiya','marukai','times','palama']
@app.route('/')
def hello_world():
    return render_template('index.html',stores=stores)

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
        
@app.route('/stores/<storeName>')
def flyer_resources(storeName):
    if storeName == 'nijiya':
        return json.dumps([
            'http://www.nijiya.com/img/sale/hi1.jpg',
            'http://www.nijiya.com/img/sale/hi2.jpg',
            'http://www.nijiya.com/img/sale/hi3.jpg',
            'http://www.nijiya.com/img/sale/hi4.jpg'])
    elif storeName == 'marukai':
        return json.dumps([
            'http://www.marukaihawaii.com/weeklyad/01012015_booklet/1/010315p1.jpg',
            'http://www.marukaihawaii.com/weeklyad/01012015_booklet/1/010315p2.jpg',
            'http://www.marukaihawaii.com/weeklyad/01012015_booklet/1/010315p3.jpg',
            'http://www.marukaihawaii.com/weeklyad/01012015_booklet/1/010315p4.jpg',
            'http://www.marukaihawaii.com/weeklyad/01012015_booklet/1/010315p5.jpg',            
            ])
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9090)
