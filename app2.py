from flask import Flask, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)


@app.before_request
def before_first_request():
    init_db()


def init_db():
    conn = get_db_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT NOT NULL)')
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def close_db_connection(conn):
    conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    # conn.execute('INSERT INTO posts (title, content) VALUES ("Why I love Flask", "This is so cool!!!")')
    # conn.execute(
    #   'INSERT INTO posts (title, content) VALUES ("Cats >> Dogs", "It was a joke because they are all so adorable.")')
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def get_post(post_id):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO posts (title, content) VALUES ("Random Title", "Lorem ipsum dolor sit amet consectetur adipiscing elit")')
    animals = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('animals.html', animals=animals)


@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('create_animalse.html')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    id = id
    conn = get_db_connection()
    conn.execute(f"""DELETE from posts where id = {id}""").fetchone()
    conn.commit()
    conn.close()
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)
