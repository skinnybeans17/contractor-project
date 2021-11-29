from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get("DB_URL")
client = MongoClient(host=host)
db = client.CharityTracker
donations = db.donations

app = Flask(__name__)

@app.route('/')
def charity_index():
    donates=list(donations.find())
    for i in range(len(donates)):
      donates[i]['amount'] = float(donates[i]['amount'])
    donates.sort(key=lambda x: x['date'], reverse=False)
    return render_template('charity_index.html', donations=donates)

@app.route('/donations/new')
def donation_new():
    return render_template('donations_new.html')

@app.route('/donations', methods=['POST'])
def donation_submit():
    donation = {
        'name': request.form.get('charity-name'),
        'amount': request.form.get('amount'),
        'date': request.form.get('date'),
    }
    donations.insert_one(donation)
    return redirect(url_for('charity_index'))

@app.route('/donations/<donation_id>/remove', methods=['POST'])
def donation_delete(donation_id):
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('charity_index'))

if __name__ == '__main__':
  app.run(debug=True)