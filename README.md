# Personen-Generator

Ein Flask-basierter Fake-Personen-Generator mit deutschen Daten. Ideal für Testzwecke.

## Features

- Realistische deutsche Personendaten
- Filter nach Geschlecht/Altersbereich
- Export in CSV, vCard, PDF
- JSON-REST-API
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
- Einzelne Person: `curl http://localhost:5000/api/person`
- Gefiltert: `curl "http://localhost:5000/filter?geschlecht=F&min=25&max=40"`

## Stack
- **Backend**: Python, Flask, Faker
- **Frontend**: Vanilla JS, CSS
- **Export**: ReportLab
- **Container**: Docker

---

MIT License – Generiert nur fiktive Daten für Testumgebungen.