import os
import openai
import requests
import json
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
Session(app)

# Ensure the upload folder exists!
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///selsoo.db")

client = openai.OpenAI()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/emotion/<string:emotion>/<int:level>")
@login_required
def emotion(emotion, level):
    return render_template(f"{emotion}{level}.html")

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must create username", 400)
        elif not password:
            return apology("must create password", 400)
        elif not confirmation:
            return apology("must repeat password", 400)
        elif password != confirmation:
            return apology("passwords must match!", 400)

        exists = db.execute("SELECT * FROM users WHERE username = ?", username)
        if exists:
            return apology("username already taken :(", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/storytime")
@login_required
def storytime():
    label = request.args.get('label')
    prompt = f"Write a meditation-style adventurous short story in the 2nd person about someone's journey finding comfort in spite of being {label}. It should be five paragraphs long. It should acknowledge the reader's own feelings of currently being {label} in the beginning. Include comforting imagery, tactile sensations, and a surrealist narrative. Avoid cliches such as lotus flowers or anything obvious. Never use the words 'meditation' or 'meditations' in the story. The story should be creative and adventurous in imagery but carry a consistent theme throughout. no more than 5 paragraphs long!!!"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a calming and creative assistant. You are a bit funny and witty too! You are concise, and never write more than you are asked to limit yourself to."},
            {"role": "user", "content": prompt},
        ],
    )

    generated_story = response.choices[0].message.content
    generated_story_html = generated_story.replace('\n\n', '<br><br>')

    prompt2 = f"Here is a story: {generated_story}. After reading that story: Within 12 words or less, describe the most unique, surreal object found within that story."
    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a precise and creative assistant. You are a bit funny and witty too!"},
            {"role": "user", "content": prompt2},
        ],
    )

    object = response2.choices[0].message.content
    generated_object = generate_image(object)

    prompt3 = f"Here is a story: {object}. After reading that story: Title the story using 4 words or less."
    response3 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a precise and creative assistant. You are a bit funny and witty too!"},
            {"role": "user", "content": prompt3},
        ],
    )

    user_id = session["user_id"]
    title = response3.choices[0].message.content.strip('"')
    db.execute("INSERT INTO stories (user_id, title, content, illustration_path, emotion) VALUES (?, ?, ?, ?, ?)",
               user_id, title, generated_story_html, generated_object, label)

    return render_template("storytime.html", generated_story=generated_story_html, object=object, generated_object=generated_object, title=title)

@app.route("/archive")
@login_required
def archive():
    user_id = session["user_id"]
    stories = db.execute("SELECT * FROM stories WHERE user_id = ? ORDER BY created_at DESC", user_id)
    return render_template("archive.html", stories=stories)

@app.route("/story/<int:story_id>")
@login_required
def view_story(story_id):
    story = db.execute("SELECT * FROM stories WHERE id = ?", story_id)
    if not story:
        return apology("Story not found", 404)
    return render_template("storytime.html", generated_story=story[0]['content'], generated_object=story[0]['illustration_path'], title=story[0]['title'])

def generate_image(text):
    response = client.images.generate(
        model="dall-e-3",
        prompt="a 3d rendered object surrealist illustration of " + text,
        n=1,
        size="1024x1024"
    )

    image_url = response.data[0].url
    return save_generated_image(image_url)

def save_generated_image(image_url):
    image_data = requests.get(image_url).content
    unique = f"generated_image_{int(time.time())}.jpg"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)
    return image_path
