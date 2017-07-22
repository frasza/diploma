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
        db.execute("INSERT INTO uporabniki(uporabniskoime, email, geslo) VALUES (?,?,?)", ([
            form.uporabniskoime.data,
            form.email.data,
            form.geslo.data
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
    cur = db.execute('SELECT id, uporabniskoime FROM uporabniki WHERE uporabniskoime = :uporabniskoime AND geslo = :geslo', request.form)
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
        "SELECT vnosi.naslov, vnosi.opis, vnosi.spremembe, vnosi.kategorija, vnosi.stroski, vnosi.odobritev, vnosi.vpliv, vnosi.vnos_id, uporabniki.uporabniskoime FROM vnosi JOIN uporabniki ON vnosi.uporabnik_id = uporabniki.id")
    vnosi = [dict(naslov=row[0], opis=row[1], spremembe=row[2], kategorija=row[3], stroski=row[4], odobritev=row[5],
                    vpliv=row[6], vnos_id=row[7], uporabnik_id=row[8]) for row in c.fetchall()]
    db.close()

    return render_template(
        "index.html",
        form=NewEntry(request.form),
        vnosi=vnosi
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
    naslov = request.form["naslov"]
    opis = request.form["opis"]
    spremembe = request.form["spremembe"]
    kategorija = request.form["kategorija"]
    stroski = request.form["stroski"]
    odobritev = request.form["odobritev"]
    vpliv = request.form["vpliv"]
    uporabnik_id = session["user_id"]
    if not naslov or not opis or not spremembe or not kategorija or not stroski or not odobritev or not vpliv:
        flash("Vsa polja so obvezna.")
        return redirect(url_for("entry"))
    else:
        db.execute(
            "INSERT INTO vnosi (naslov, opis, spremembe, kategorija, stroski, odobritev, vpliv, uporabnik_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                naslov,
                opis,
                spremembe,
                kategorija,
                stroski,
                odobritev,
                vpliv,
                uporabnik_id
            ]
        )
        db.commit()
        db.close()
        flash("Nov vnos je bil uspešno zapisan.")
        return redirect(url_for("index"))


@app.route("/izkusnja/<int:vnos_id>/")
# @login_required
def izkusnja(vnos_id):
    db = connect_db()

    c = db.execute(
        "SELECT vnosi.naslov, vnosi.opis, vnosi.spremembe, vnosi.kategorija, vnosi.stroski, vnosi.odobritev, vnosi.vpliv, vnosi.vnos_id, uporabniki.uporabniskoime FROM vnosi JOIN uporabniki ON vnosi.uporabnik_id = uporabniki.id WHERE vnos_id=?",
        [vnos_id])

    vnosi = [dict(naslov=row[0], opis=row[1], spremembe=row[2], kategorija=row[3], stroski=row[4], odobritev=row[5],
                    vpliv=row[6], vnos_id=row[7], uporabnik_id=row[8]) for row in c.fetchall()]

    return render_template("izkusnja.html", vnosi=vnosi)


@app.route("/uspesnost/")
# @login_required
def success():
    return render_template('kategorije.html')


@app.route("/uspesnost_kategorije/<kategorija>/")
# @login_required
def category_success(kategorija):
    db = connect_db()

    c = db.execute(
        "SELECT vnosi.naslov, vnosi.opis, vnosi.spremembe, vnosi.kategorija, vnosi.stroski, vnosi.odobritev, vnosi.vpliv, vnosi.vnos_id, uporabniki.uporabniskoime FROM vnosi JOIN uporabniki ON vnosi.uporabnik_id = uporabniki.id WHERE kategorija=?",
        [kategorija])

    vnosi = [dict(naslov=row[0], opis=row[1], spremembe=row[2], kategorija=row[3], stroski=row[4], odobritev=row[5],
                    vpliv=row[6], vnos_id=row[7], uporabnik_id=row[8]) for row in c.fetchall()]

    c = db.execute("SELECT COUNT(vpliv) FROM vnosi WHERE kategorija = ? GROUP BY vpliv", [kategorija])
    priorityLabels = c.fetchall()

    c = db.execute("SELECT odobritev FROM vnosi WHERE kategorija = ? GROUP BY odobritev", [kategorija])
    approvalLabels = c.fetchall()

    c = db.execute("SELECT stroski FROM vnosi WHERE kategorija = ? GROUP BY stroski", [kategorija])
    costsLabels = c.fetchall()

    c = db.execute("SELECT vpliv FROM vnosi WHERE kategorija = ? GROUP BY vpliv", [kategorija])
    stevilke = c.fetchall()

    c = db.execute(
        "SELECT 100 * count(*) / (SELECT count(*) FROM vnosi WHERE kategorija = ?) FROM vnosi WHERE kategorija = ? GROUP BY odobritev",
        [kategorija, kategorija])
    approvalValues = c.fetchall()

    c = db.execute(
        "SELECT 100 * count(*) / (SELECT count(*) FROM vnosi WHERE kategorija = ?) FROM vnosi WHERE kategorija = ? GROUP BY stroski",
        [kategorija, kategorija])
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

    return render_template("uspesnost_kategorije.html", approvalLabels=approvalLabels, costsLabels=costsLabels, vnosi=vnosi,
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


@app.route('/delete/<int:vnos_id>')
@login_required
def delete_entry(vnos_id):
    db = connect_db()
    
    db.execute('DELETE FROM vnosi WHERE vnos_id ='+str(vnos_id))

    db.commit()
    db.close()
    return redirect(url_for('index'))