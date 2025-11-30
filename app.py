from flask import Flask, render_template, request, jsonify, send_file, Response
from faker import Faker
import csv
import json
from io import BytesIO, StringIO
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import qrcode
import secrets
import string

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

def generate_password(length=12):
    """Generiert ein sicheres zufälliges Passwort."""
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

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
                'Passwort': generate_password(),
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
    count = request.args.get('count', default=100, type=int)
    # Limit auf max 10000 Personen
    count = min(count, 10000)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        'Name', 'Geschlecht', 'Geburtsdatum', 'Alter', 'Adresse', 'Telefon',
        'E-Mail', 'Benutzername', 'Passwort', 'Beruf', 'Firma', 'IBAN', 'BIC'
    ])
    writer.writeheader()
    for _ in range(count):
        writer.writerow(generate_person())
    output.seek(0)
    return send_file(
        BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'personen_{count}.csv'
    )

@app.route('/api/person')
def api_person():
    return jsonify(generate_person())

@app.route('/api/persons')
def api_persons():
    """Batch API endpoint für mehrere Personen."""
    count = request.args.get('count', default=10, type=int)
    # Limit auf max 1000 Personen für API
    count = min(count, 1000)

    geschlecht = request.args.get('geschlecht')
    min_alter = request.args.get('min', default=18, type=int)
    max_alter = request.args.get('max', default=75, type=int)

    persons = []
    max_tries = count * 100  # Genug Versuche für gefilterte Anfragen
    tries = 0

    while len(persons) < count and tries < max_tries:
        tries += 1
        person = generate_person()

        # Filter anwenden wenn angegeben
        if geschlecht and person['Geschlecht'] != geschlecht:
            continue
        if not (min_alter <= person['Alter'] <= max_alter):
            continue

        persons.append(person)

    return jsonify({'count': len(persons), 'persons': persons})

@app.route('/download-json')
def download_json():
    """JSON Export mit konfigurierbarer Anzahl."""
    count = request.args.get('count', default=100, type=int)
    # Limit auf max 10000 Personen
    count = min(count, 10000)

    persons = [generate_person() for _ in range(count)]

    output = BytesIO()
    output.write(json.dumps({'count': count, 'persons': persons}, indent=2, ensure_ascii=False).encode('utf-8'))
    output.seek(0)

    return send_file(
        output,
        mimetype='application/json',
        as_attachment=True,
        download_name=f'personen_{count}.json'
    )

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

@app.route('/vcard-qr')
def vcard_qr():
    """Generiert QR-Code für vCard Daten."""
    # Person aus Session oder neue generieren
    # Für Einfachheit generieren wir eine neue Person
    person = generate_person()

    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{person['Name']}
EMAIL:{person['E-Mail']}
TEL:{person['Telefon']}
ADR;TYPE=home:;;{person['Adresse']}
ORG:{person['Firma']}
TITLE:{person['Beruf']}
END:VCARD"""

    # QR-Code generieren
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(vcard)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # In BytesIO speichern
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

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