from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charity = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        donation_content = request.form['content']
        new_donation = Todo(content=donation_content)

        try:
            db.session.add(new_donation)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your donation'

    else:
        donations = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', donations=donations)


@app.route('/delete/<int:id>')
def delete(id):
    donation_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(donation_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that donation'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    donation = Todo.query.get_or_404(id)

    if request.method == 'POST':
        donation.charity = request.form['charity']
        donation.amount = request.form['amount']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your donation'

    else:
        return render_template('update.html', donation=donation)


if __name__ == "__main__":
    app.run(debug=True)
