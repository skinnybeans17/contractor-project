from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

host = os.environ.get("DB_URL")
client = MongoClient(host=host)
db = client.CharityTracker
donations = db.donations

app = Flask(__name__)

@app.route('/')
def index(): 
    donates=list(donations.find())
    for i in range(len(donates)):
      donates[i]['amount'] = float(donates[i]['amount'])
    donates.sort(key=lambda x: x['date'], reverse=False)
    return render_template("index.html", donations=donates)

@app.route('/donations/new')
def donation_new():
    return render_template('new_donation.html')

@app.route('/donations', methods=['POST'])
def donation_submit():
    donation = {
        'name': request.form.get('name'),
        'amount': request.form.get('amount'),
        'date': datetime.now()
      }
    donations.insert_one(donation)
    return redirect(url_for('index'))

@app.route('/donations/<donation_id>/remove', methods=['POST'])
def donation_del(donation_id):
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)