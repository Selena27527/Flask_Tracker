from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    status = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def index():
    all_games = Game.query.all()
    return render_template('index.html', games=all_games)

@app.route('/add', methods=['POST'])
def add_game():
    new_game = Game(
        title=request.form.get('title'),
        platform=request.form.get('platform'),
        rating=int(request.form.get('rating')),
        status=request.form.get('status')
    )
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_game(id):
    game = Game.query.get_or_404(id)
    if request.method == 'POST':
        game.title = request.form.get('title')
        game.platform = request.form.get('platform')
        game.rating = int(request.form.get('rating'))
        game.status = request.form.get('status')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', game=game)

@app.route('/delete/<int:id>')
def delete_game(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/suggest')
def suggest():
    # Only pick from games that are in the 'Backlog'
    backlog_games = Game.query.filter_by(status='Backlog').all()
    selected_game = random.choice(backlog_games) if backlog_games else None
    return render_template('suggest.html', game=selected_game)

if __name__ == '__main__':
    app.run(debug=True, port=5001)