from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

CONNECTION_STRING= "mongodb+srv://applicationHA:tesnoh-zixqa5-Ciwkip@cluster0.wxmxq.mongodb.net/CharityTracker?retryWrites=true&w=majority"
host = os.environ.get("DB_URL")
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_default_database()
donations = db.donations
charities = db.charities

app = Flask(__name__)

@app.route('/')
def index():
    donated=list(donations.find())
    for i in range(len(donated)):
      donated[i]['amount'] = float(donated[i]['amount'])
    donated.sort(key=lambda x: x['date'], reverse=False)
    return render_template('donations_index.html', donations=donated)

@app.route('/donations/new')
def donation_new():
    return render_template('new_donation.html')

@app.route('/donations', methods=['POST'])
def donation_submit():
    donation = {
        'name': request.form.get('charity-name'),
        'amount': '$' + request.form.get('amount'),
        'date': request.form.get('date'),
    }
    donations.insert_one(donation)
    return redirect(url_for('index'))

@app.route('/donations/<donation_id>/remove', methods=['POST'])
def donation_delete(donation_id):
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('index'))

#---------------------------------------------------------------------

@app.route('/charities')
def charities_index():
    return render_template('charities_index.html', charities=charities.find())

@app.route('/charities/new', methods=['POST'])
def charities_new():
    return render_template('new_charity.html')

@app.route('/charities', methods=['POST'])
def charitity_submit():
    charity = {
        'charity-name': request.form.get('charity-name')
    }
    charities.insert_one(charity)
    return redirect(url_for('charities_index'))

@app.route('/charities/<charity_name>/edit')
def charity_edit(charity_name):
    charity = charities.find_one({'name': charity_name})
    return render_template('charity_edit.html', charity=charity, title='Edit Charity')

@app.route('/charities/<charity_name>', methods=['POST'])
def charity_update(charity_name):
    updated_charity = {
        'charity-name': request.form.get('charity_name')
    }
    charities.update_one(
        {'name': charity_name},
        {'set': updated_charity} 
    )
    return redirect(url_for('charities_index'))

if __name__ == '__main__':
  app.run(debug=True)