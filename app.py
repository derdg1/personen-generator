from flask import Flask, render_template, request, jsonify, send_file, Response
from faker import Faker
import csv
from io import BytesIO, StringIO
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)
fake = Faker('de_DE')

# Titel, die wir im Namen ausschließen wollen
titelworte = ['Dr.', 'Prof.', 'Dipl.', 'Dipl.-Ing.', 'Mag.', 'B.Sc.', 'M.Sc.']

def calculate_age(birth_date):
    """Berechnet das genaue Alter basierend auf dem Geburtsdatum."""
    today = date.today()
    age = today.year - birth_date.year
    # Prüfen ob Geburtstag in diesem Jahr schon war
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

def generate_person():
    while True:
        profile = fake.simple_profile()
        name = profile['name']
        # Namen mit Titeln aussortieren
        if not any(titel in name for titel in titelworte):
            geburtsdatum = fake.date_of_birth(minimum_age=18, maximum_age=75)
            return {
                'Name': name,
                'Geschlecht': profile['sex'],
                'Geburtsdatum': geburtsdatum.strftime('%Y-%m-%d'),
                'Alter': calculate_age(geburtsdatum),
                'Adresse': fake.address().replace('\n', ', '),
                'Telefon': fake.phone_number(),
                'E-Mail': profile['mail'],
                'Benutzername': profile['username'],
                'Beruf': fake.job(),
                'Firma': fake.company(),
                'IBAN': fake.iban(),
                'BIC': fake.swift()
            }

@app.route('/')
def index():
    person = generate_person()
    return render_template('index.html', person=person)

@app.route('/filter')
def filter_person():
    geschlecht = request.args.get('geschlecht')
    min_alter = request.args.get('min', default=18, type=int)
    max_alter = request.args.get('max', default=75, type=int)

    max_tries = 1000
    tries = 0

    while tries < max_tries:
        tries += 1
        person = generate_person()
        if geschlecht and person['Geschlecht'] != geschlecht:
            continue
        if not (min_alter <= person['Alter'] <= max_alter):
            continue
        return render_template('index.html', person=person)

    return "Keine Person gefunden, die den Kriterien entspricht.", 404

@app.route('/download-csv')
def download_csv():
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        'Name', 'Geschlecht', 'Geburtsdatum', 'Alter', 'Adresse', 'Telefon',
        'E-Mail', 'Benutzername', 'Beruf', 'Firma', 'IBAN', 'BIC'
    ])
    writer.writeheader()
    for _ in range(100):
        writer.writerow(generate_person())
    output.seek(0)
    return send_file(
        BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='personen.csv'
    )

@app.route('/api/person')
def api_person():
    return jsonify(generate_person())

@app.route('/download-vcard')
def download_vcard():
    person = generate_person()
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{person['Name']}
EMAIL:{person['E-Mail']}
TEL:{person['Telefon']}
ADR;TYPE=home:;;{person['Adresse']}
ORG:{person['Firma']}
TITLE:{person['Beruf']}
END:VCARD
"""
    return Response(vcard, mimetype='text/vcard',
                    headers={'Content-Disposition': 'attachment; filename=person.vcf'})

@app.route('/download-pdf')
def download_pdf():
    person = generate_person()

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Schriftgröße & Position
    c.setFont("Helvetica", 14)
    y = height - 50

    c.drawString(50, y, "Personendaten")
    y -= 30

    for key, value in person.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20
        if y < 50:  # neue Seite falls nötig
            c.showPage()
            c.setFont("Helvetica", 14)
            y = height - 50

    c.save()
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='person.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)