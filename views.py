import sqlite3

from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sslify import SSLify

from forms import NewEntry, RegisterForm, LoginForm

from flask_mail import Mail, Message

# Config
app = Flask(__name__)
app.config.from_object("_config")

sslify = SSLify(app)

mail = Mail(app)


# Helper functions
def connect_db():
    return sqlite3.connect(app.config["DATABASE_PATH"], timeout=10)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return test(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrap


# Register route
@app.route("/registracija/", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        db = connect_db()
        db.execute("INSERT INTO users(name, email, password) VALUES (?,?,?)", ([
            form.name.data,
            form.email.data,
            form.password.data
        ]))
        db.commit()
        db.close()

        # Thank you mail for registration
        msg = Message(
            "Dobrodošli v skupnosti!",
            recipients=[form.email.data]
        )
        msg.html = render_template("mail.html")
        mail.send(msg)

        return redirect(url_for("index"))

    return render_template("registracija.html", form=form)


# Routes
@app.route("/odjava/")
def logout():
    session.pop("logged_in", None)
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route('/prijava/', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method != "POST" or not form.validate():
        return render_template('login.html')
    db = connect_db()
    cur = db.execute('SELECT id, name FROM users WHERE name = :name AND password = :password', request.form)
    users = cur.fetchall()
    if len(users) == 1:
        session['logged_in'] = True
        session["user_id"] = users[0][0]
        session["username"] = users[0][1]
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route("/", methods=["GET", "POST"])
def index():
    db = connect_db()

    c = db.execute(
        "SELECT entries.title, entries.description, entries.changes, entries.category, entries.costs, entries.approval, entries.work, entries.entry_id, users.name FROM entries JOIN users ON entries.user_id = users.id")
    entries = [dict(title=row[0], description=row[1], changes=row[2], category=row[3], costs=row[4], approval=row[5],
                    work=row[6], entry_id=row[7], user_id=row[8]) for row in c.fetchall()]

    db.close()

    return render_template(
        "index.html",
        form=NewEntry(request.form),
        entries=entries
    )


@app.route('/vpis_izkusnje/')
@login_required
def entry():
    return render_template("vpis_izkusnje.html")


# Add new entry
@app.route("/nova_izkusnja/", methods=["POST"])
@login_required
def new_entry():
    db = connect_db()
    title = request.form["title"]
    description = request.form["description"]
    changes = request.form["changes"]
    category = request.form["category"]
    costs = request.form["costs"]
    approval = request.form["approval"]
    work = request.form["work"]
    user_id = session["user_id"]
    if not title or not description or not changes or not category or not costs or not approval or not work:
        flash("All fields are required. Please try again.")
        return redirect(url_for("entry"))
    else:
        db.execute(
            "INSERT INTO entries (title, description, changes, category, costs, approval, work, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                title,
                description,
                changes,
                category,
                costs,
                approval,
                work,
                user_id
            ]
        )
        db.commit()
        db.close()
        flash("New entry was successfully posted.")
        return redirect(url_for("index"))


@app.route("/izkusnja/<int:entry_id>/")
# @login_required
def izkusnja(entry_id):
    db = connect_db()

    c = db.execute(
        "SELECT entries.title, entries.description, entries.changes, entries.category, entries.costs, entries.approval, entries.work, entries.entry_id, users.name FROM entries JOIN users ON entries.user_id = users.id WHERE entry_id=?",
        [entry_id])

    entries = [dict(title=row[0], description=row[1], changes=row[2], category=row[3], costs=row[4], approval=row[5],
                    work=row[6], entry_id=row[7], user_id=row[8]) for row in c.fetchall()]
    """
    c = db.execute("SELECT COUNT(priority) AS sestevek FROM tasks GROUP BY priority")
    sestevek = c.fetchall()

    c = db.execute("SELECT priority AS stevilke FROM tasks GROUP BY priority")
    stevilke = c.fetchall()

    c = db.execute("SELECT count(*) * 100 / (SELECT count(*) from tasks) FROM tasks GROUP BY priority")
    odst = c.fetchall()

    db.close()

    prio = [x[0] for x in sestevek]
    stev = [x[0] for x in stevilke]
    odstotek = [x[0] for x in odst]

    legend = "Priority Frequency"
    legend_pie = "Priority %"
    labels = stev
    values = prio

    values=values, labels=labels, legend=legend, legend_pie=legend_pie, odstotek=odstotek
    """

    return render_template("izkusnja.html", entries=entries)


@app.route("/uspesnost/")
# @login_required
def success():
    return render_template('kategorije.html')


@app.route("/uspesnost_kategorije/<category>/")
# @login_required
def category_success(category):
    db = connect_db()

    c = db.execute(
        "SELECT entries.title, entries.description, entries.changes, entries.category, entries.costs, entries.approval, entries.work, entries.entry_id, users.name FROM entries JOIN users ON entries.user_id = users.id WHERE category=?",
        [category])

    entries = [dict(title=row[0], description=row[1], changes=row[2], category=row[3], costs=row[4], approval=row[5],
                    work=row[6], entry_id=row[7], user_id=row[8]) for row in c.fetchall()]

    c = db.execute("SELECT COUNT(work) FROM entries WHERE category = ? GROUP BY work", [category])
    priorityLabels = c.fetchall()

    c = db.execute("SELECT approval FROM entries WHERE category = ? GROUP BY approval", [category])
    approvalLabels = c.fetchall()

    c = db.execute("SELECT costs FROM entries WHERE category = ? GROUP BY costs", [category])
    costsLabels = c.fetchall()

    c = db.execute("SELECT work FROM entries WHERE category = ? GROUP BY work", [category])
    stevilke = c.fetchall()

    c = db.execute(
        "SELECT 100 * count(*) / (SELECT count(*) FROM entries WHERE category = ?) FROM entries WHERE category = ? GROUP BY approval",
        [category, category])
    approvalValues = c.fetchall()

    c = db.execute(
        "SELECT 100 * count(*) / (SELECT count(*) FROM entries WHERE category = ?) FROM entries WHERE category = ? GROUP BY costs",
        [category, category])
    costsValues = c.fetchall()

    db.close()

    priorityLabels = [x[0] for x in priorityLabels]
    approvalLabels = [x[0] for x in approvalLabels]
    costsLabels = [x[0] for x in costsLabels]
    labels = [x[0] for x in stevilke]
    approvalValues = [x[0] for x in approvalValues]
    costsValues = [x[0] for x in costsValues]

    legend = "Frekvenca"
    legend_pie = "Priority %"

    return render_template("uspesnost_kategorije.html", approvalLabels=approvalLabels, costsLabels=costsLabels, entries=entries,
                           priorityLabels=priorityLabels, labels=labels, legend=legend, legend_pie=legend_pie,
                           approvalValues=approvalValues, costsValues=costsValues)


@app.route("/o_als/")
# @login_required
def als():
    return render_template('o_als.html')

@app.route("/stevilke/")
# @login_required
def stevilke():
    return render_template('stevilke.html')