from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField, PasswordField, Form, BooleanField, validators, \
    ValidationError


class NewEntry(Form):
    entry_id = IntegerField()
    title = StringField("Naslov", [validators.Required("Vnesite naslov izkušnje")])
    description = StringField("Opis", [validators.Required("Vnesite opis izkušnje")])
    changes = StringField("Spremembe", [validators.Required("Vnesite opažene spremembe")])
    category = SelectField("Kategorija", [validators.Required("Izberite kategorijo")],
                           choices=[
                               ("Prehrana", "Prehrana"), ("Fizična aktivnost", "Fizična aktivnost"),
                               ("Uporaba pripomočkov", "Uporaba pripomočkov"), ("Terapija", "Terapija"),
                               ("Zdravila", "Zdravila"),
                           ]
                           )
    costs = SelectField("Stroški", [validators.Required("Izberite mesečne stroške")],
                        choices=[
                            ("10-50 €", "10-50 €"), ("50-100 €", "50-100 €"), ("100-500 €", "100-500 €"),
                            ("500-1000 €", "500-1000 €"), ("Več kot 1000 € mesečno", "Več kot 1000 € mesečno"),
                        ]
                        )
    approval = SelectField("Podpora", [validators.Required("Vnesite ali je vaša izkušnja podprta s strani medicine")],
                           choices=[
                               ("Da", "Da"), ("Ne", "Ne"), ("Nevem", "Nevem"),
                           ])
    work = SelectField("Delovanje", [validators.Required("Vnesite kako se vam zdi da deluje")],
                       choices=[
                           ("Sploh ni pomagalo", "Sploh ni pomagalo"), ("Ni pomagalo", "Ni pomagalo"),
                           ("Niti niti", "Niti nit"), ("Je pomagalo", "Je pomagalo"),
                           ("Zelo je pomagalo", "Zelo je pomagalo"),
                       ])
    user_id = IntegerField()


class RegisterForm(Form):
    name = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    name = StringField(
        'Username',
        [validators.Required()]
    )
    password = PasswordField(
        'Password',
        [validators.Required()]
    )
