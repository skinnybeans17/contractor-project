from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get("DB_URL")
client = MongoClient(host=host)
db = client.get_database("contractor-project")
donations = db.donations
charities = db.charities

app = Flask(__name__)

@app.route('/')
def charities_index():
  return render_template('index.html', charities=charities.find())

@app.route('/charities/new')
def charities_new():
    charity = []
    return render_template('charities_new.html', charity=charity)

@app.route('/charities', methods=['POST'])
def charity_submit():
  charity = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
  }
  charities.insert_one(charity)
  return redirect(url_for('charities_index'))

@app.route('/charities/<charity_id>')
def charities_show(charity_id):
  charity = charities.find_one({'_id': ObjectId(charity_id)})
  charity_donations = donations.find({'charity_id': charity_id})
  return render_template('charities_show.html', charity=charity, donations=charity_donations)

@app.route('/charities/<charity_id>/edit')
def charities_edit(charity_id):
  charity = charities.find_one({'_id': ObjectId(charity_id)})
  return render_template('charities_edit.html', charity=charity)

@app.route('/charities/<charity_id>', methods=['POST'])
def charities_update(charity_id):
  updated_charity = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
  }
  charities.update_one(
    {'_id': ObjectId(charity_id)},
    {'$set': updated_charity})
  return redirect(url_for('charities_show', charity_id=charity_id))

@app.route('/charities/<charity_id>/delete', methods=['POST'])
def charities_delete(charity_id):
  charities.delete_one({'_id': ObjectId(charity_id)})
  return redirect(url_for('charities_index'))

@app.route('/charities/donations', methods=['POST'])
def donations_new():
  charity_id = request.form.get("charity_id")
  donation = {
    'charity_id': charity_id,
    'amount': request.form.get('amount'),
    'date': request.form.get('date'),
  }
  donations.insert_one(donation)
  return redirect(url_for('charities_show', charity_id=charity_id))

@app.route('/charities/<charities_id>/donations/<donation_id>/delete')
def delete_donation(charity_id, donation_id):
  donation = donations.find_one({'_id': ObjectId(donation_id)})
  charity_id = donation['charity_id']
  donations.delete_one({'_id': ObjectId(donation_id)})
  return redirect(url_for('charities_show', charity_id=charity_id))

if __name__ == '__main__':
  app.run(debug=True)