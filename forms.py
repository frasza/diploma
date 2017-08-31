from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField, PasswordField, Form, BooleanField, validators, \
    ValidationError


class NewEntry(Form):
    vnos_id = IntegerField()
    naslov = StringField("Naslov", [validators.Required("Vnesite naslov izkušnje")])
    opis = StringField("Opis", [validators.Required("Vnesite opis izkušnje")])
    spremembe = StringField("Spremembe", [validators.Required("Vnesite opažene spremembe")])
    kategorija = SelectField("Kategorija", [validators.Required("Izberite kategorijo")],
                           choices=[
                               ("Prehrana", "Prehrana"), ("Fizična aktivnost", "Fizična aktivnost"),
                               ("Uporaba pripomočkov", "Uporaba pripomočkov"), ("Terapija", "Terapija"),
                               ("Zdravila", "Zdravila"),("Drugo", "Drugo"),
                           ]
                           )
    stroski = SelectField("Stroški", [validators.Required("Izberite stroške")],
                        choices=[
                            ("Ni stroškov", "Ni stroškov"), ("10-50 €", "10-50 €"), ("50-100 €", "50-100 €"), ("100-500 €", "100-500 €"),
                            ("500-1000 €", "500-1000 €"), ("Več kot 1000 €", "Več kot 1000 €"),
                        ]
                        )
    odobritev = SelectField("Odobritev", [validators.Required("Vnesite ali je vaša izkušnja podprta / odobrena s strani medicine")],
                           choices=[
                               ("Da", "Da"), ("Ne", "Ne"), ("Ne vem", "Ne vem"),
                           ])
    vpliv = SelectField("Vpliv", [validators.Required("Kako se vam zdi, da je izkusnja vplivala na pocutje bolnika?")],
                       choices=[
                           ("Zelo negativno", "Zelo negativno"), ("Negativno", "Negativno"),
                           ("Niti negativno niti pozitivno", "Niti negativno niti pozitivno"), ("Pozitivno", "Pozitivno"),
                           ("Zelo pozitivno", "Zelo pozitivno"),
                       ])
    spol = SelectField("Spol", [validators.Required("Spol bolnika")],
                           choices=[
                               ("Moški", "Moški"), ("Ženski", "Ženski"),
                           ])
    starost = IntegerField()
    uporabnik_id = IntegerField()


class RegisterForm(Form):
    uporabniskoime = StringField('Uporabnisko ime', [validators.Length(min=4, max=25)])
    email = StringField('Email naslov', [validators.Length(min=6, max=35)])
    geslo = PasswordField('Geslo', [
        validators.Required(),
        validators.EqualTo('confirm', message='Gesla se morata ujemati')
    ])
    confirm = PasswordField('Ponovno geslo')


class LoginForm(Form):
    uporabniskoime = StringField(
        'Uporabnisko Ime',
        [validators.Required()]
    )
    geslo = PasswordField(
        'Geslo',
        [validators.Required()]
    )