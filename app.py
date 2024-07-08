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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///selsoo.db")

client = openai.OpenAI()

# Directory to save the generated image
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists!
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



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

@app.route("/negative")
@login_required
def negative():
    return render_template("negative.html")

@app.route("/sad")
@login_required
def sad():
    return render_template("sad.html")

@app.route("/sad1")
@login_required
def sad1():
    return render_template("sad1.html")

@app.route("/sad2")
@login_required
def sad2():
    return render_template("sad2.html")

@app.route("/sad3")
@login_required
def sad3():
    return render_template("sad3.html")

@app.route("/sad4")
@login_required
def sad4():
    return render_template("sad4.html")

@app.route("/angry")
@login_required
def angry():
    return render_template("angry.html")

@app.route("/angry1")
@login_required
def angry1():
    return render_template("angry1.html")

@app.route("/angry2")
@login_required
def angry2():
    return render_template("angry2.html")

@app.route("/angry3")
@login_required
def angry3():
    return render_template("angry3.html")

@app.route("/angry4")
@login_required
def angry4():
    return render_template("angry4.html")

@app.route("/apathetic")
@login_required
def apathetic():
    return render_template("apathetic.html")

@app.route("/apathetic1")
@login_required
def apathetic1():
    return render_template("apathetic1.html")

@app.route("/apathetic2")
@login_required
def apathetic2():
    return render_template("apathetic2.html")

@app.route("/apathetic3")
@login_required
def apathetic3():
    return render_template("apathetic3.html")

@app.route("/apathetic4")
@login_required
def apathetic4():
    return render_template("apathetic4.html")

@app.route("/anxious")
@login_required
def anxious():
    return render_template("anxious.html")

@app.route("/anxious1")
@login_required
def anxious1():
    return render_template("anxious1.html")

@app.route("/anxious2")
@login_required
def anxious2():
    return render_template("anxious2.html")

@app.route("/anxious3")
@login_required
def anxious3():
    return render_template("anxious3.html")

@app.route("/anxious4")
@login_required
def anxious4():
    return render_template("anxious4.html")

@app.route("/uncomfortable")
@login_required
def uncomfortable():
    return render_template("uncomfortable.html")

@app.route("/uncomfortable1")
@login_required
def uncomfortable1():
    return render_template("uncomfortable1.html")

@app.route("/uncomfortable2")
@login_required
def uncomfortable2():
    return render_template("uncomfortable2.html")

@app.route("/uncomfortable3")
@login_required
def uncomfortable3():
    return render_template("uncomfortable3.html")

@app.route("/uncomfortable4")
@login_required
def uncomfortable4():
    return render_template("uncomfortable4.html")

@app.route("/shocked")
@login_required
def shocked():
    return render_template("shocked.html")

@app.route("/shocked1")
@login_required
def shocked1():
    return render_template("shocked1.html")

@app.route("/shocked2")
@login_required
def shocked2():
    return render_template("shocked2.html")

@app.route("/shocked3")
@login_required
def shocked3():
    return render_template("shocked3.html")

@app.route("/shocked4")
@login_required
def shocked4():
    return render_template("shocked4.html")

@app.route("/tired")
@login_required
def tired():
    return render_template("tired.html")

@app.route("/tired1")
@login_required
def tired1():
    return render_template("tired1.html")

@app.route("/tired2")
@login_required
def tired2():
    return render_template("tired2.html")

@app.route("/tired3")
@login_required
def tired3():
    return render_template("tired3.html")

@app.route("/tired4")
@login_required
def tired4():
    return render_template("tired4.html")

@app.route("/sick")
@login_required
def sick():
    return render_template("sick.html")

@app.route("/sick1")
@login_required
def sick1():
    return render_template("sick1.html")

@app.route("/sick2")
@login_required
def sick2():
    return render_template("sick2.html")

@app.route("/sick3")
@login_required
def sick3():
    return render_template("sick3.html")

@app.route("/sick4")
@login_required
def sick4():
    return render_template("sick4.html")

@app.route("/sick5")
@login_required
def sick5():
    return render_template("sick5.html")

@app.route("/sick6")
@login_required
def sick6():
    return render_template("sick6.html")

@app.route("/sick7")
@login_required
def sick7():
    return render_template("sick7.html")

@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must create username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must create password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must repeat password", 400)

        # Ensure passwords match!
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match!", 400)

        # Query database for username
        exists = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username doesn't exist
        if len(exists) > 0:
            return apology("username already taken :( ", 400)

        # add user to database
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password)

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/storytime")
@login_required
def storytime():
    # Get the label from the URL query parameter for emotion selected
    label = request.args.get('label')

    # Create the prompt
    prompt = f"Write a meditation-style adventurous short story in the 2nd person about someone's journey finding comfort in spite of being {label}. it should be five paragraphs long. It should acknowledge the reader's own feelings of currently being {label} in the beginning. Include comforting imagery, tactile sensations, and a surrealist narrative. Avoid cliches such as lotus flowers or anything obvious. Never use the words 'meditation' or 'meditations' in the story. The story should be creative and adventurous in imagery but carry a consistent theme throughout. no more than 5 paragraphs long!!!"

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the appropriate engine
        messages=[
            {"role": "system", "content": "You are a calming and creative assistant. You are a bit funny and witty too! You are concise, and never write more than you are asked to limit yourself to."},
            {"role": "user", "content": prompt},
        ],
    )

    # Get the generated story from the OpenAI response
    generated_story = response.choices[0].message.content
    generated_story_html = generated_story.replace('\n\n', '<br><br>')

    prompt2 = f"Here is a story: {generated_story}. After reading that story: Within 12 words or less, describe the most unique, surreal object found within that story."

    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the appropriate engine
        messages=[
            {"role": "system", "content": "You are a precise and creative assistant. You are a bit funny and witty too!"},
            {"role": "user", "content": prompt2},
        ],
    )

    object = response2.choices[0].message.content
    generated_object = generate(object)

    prompt3 = f"Here is a story: {object}. After reading that story: Title the story using 4 words or less."

    response3 = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the appropriate engine
        messages=[
            {"role": "system", "content": "You are a precise and creative assistant. You are a bit funny and witty too!"},
            {"role": "user", "content": prompt3},
        ],
    )

    # Save the generated story to the database
    user_id = session["user_id"]
    title = response3.choices[0].message.content.strip('"')
    content = generated_story_html
    illustration_path = generated_object  # this is the url of where the jpg is located in app, not jpg itself
    emotion = label
    db.execute("INSERT INTO stories (user_id, title, content, illustration_path, emotion) VALUES (?, ?, ?, ?, ?)",
               user_id, title, content, illustration_path, emotion)


    # Render the storytime.html template with the generated story
    return render_template("storytime.html", generated_story=generated_story_html, object=object, generated_object=generated_object, title=title)

@app.route("/archive")
@login_required
def archive():
    user_id = session["user_id"]
    stories = db.execute("SELECT * FROM stories WHERE user_id = ? ORDER BY created_at DESC", user_id)
    return render_template("archive.html", stories=stories)

@app.route("/<int:story_id>")
@login_required
def view_story(story_id):
    story = db.execute("SELECT * FROM stories WHERE id = ?", story_id)

    if not story:
        return apology("Story not found", 404)

    return render_template("storytime.html", generated_story=story[0]['content'], generated_object=story[0]['illustration_path'], title=story[0]['title'])



def generate(text):
    image_url = generate_image(text)
    return image_url

def generate_image(text):
    response = client.images.generate(
        model="dall-e-3",
        prompt="a 3d rendered object surrealist illustration of " + text,
        n=1,
        size="1024x1024"
    )

    image_url = response.data[0].url
    image_url = save_generated_image(response.json())
    return image_url

def save_generated_image(response_json):
    try:
        # If response_json is a string, try to load it as JSON
        if isinstance(response_json, str):
            response_json = json.loads(response_json)

        # Check if 'url' is present in the response
        if 'url' in response_json['data'][0]:
            image_url = response_json['data'][0]['url']
            image_data = requests.get(image_url).content

            unique = f"generated_image_{int(time.time())}.jpg"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)

            with open(image_path, 'wb') as image_file:
                image_file.write(image_data)
            return image_path
        else:
            print("Error: 'url' not found in response.")
            return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"Error in save_generated_image: {e}")
        return None