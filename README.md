# Personen-Generator

Ein Flask-basierter Fake-Personen-Generator mit deutschen Daten. Ideal für Testzwecke.

## Features

- Realistische deutsche Personendaten (inkl. Passwörter)
- Filter nach Geschlecht/Altersbereich
- Export in CSV, JSON, vCard, PDF mit konfigurierbarer Anzahl
- JSON-REST-API mit Batch-Endpoint
- QR-Code für vCard-Daten
- Kopieren-Button für einzelne Felder
- PWA und Docker-Unterstützung
- Dark Mode

## Installation

### Lokal
```bash
git clone https://github.com/derdg1/personen-generator.git
cd personen-generator
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
# Öffnen: http://localhost:5000
```

### Docker
```bash
docker-compose up -d
# oder
docker build -t personen-generator .
docker run -p 5000:5000 personen-generator
# Fertiges Image: `ghcr.io/derdg1/personen-generator:latest`
```

## API

### Einzelne Person
```bash
curl http://localhost:5000/api/person
```

### Mehrere Personen (Batch)
```bash
# 50 Personen
curl "http://localhost:5000/api/persons?count=50"

# 20 Frauen zwischen 25-40 Jahren
curl "http://localhost:5000/api/persons?count=20&geschlecht=F&min=25&max=40"
```

### Gefilterte Einzelperson
```bash
curl "http://localhost:5000/filter?geschlecht=F&min=25&max=40"
```

### Export-Endpoints
- CSV: `/download-csv?count=100`
- JSON: `/download-json?count=100`
- vCard: `/download-vcard`
- PDF: `/download-pdf`
- QR-Code: `/vcard-qr`

## Stack
- **Backend**: Python, Flask, Faker
- **Frontend**: Vanilla JS, CSS
- **Export**: ReportLab, qrcode
- **Container**: Docker

---

MIT License – Generiert nur fiktive Daten für Testumgebungen.