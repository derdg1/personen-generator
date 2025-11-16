# Personen-Generator

Ein Flask-basierter Fake-Personen-Generator mit deutschen Personendaten. Generiert realistische, aber fiktive Personendaten für Testzwecke.

## Features

- **Personendaten-Generierung**: Erstellt realistische deutsche Personendaten mit Namen, Adressen, Kontaktdaten, Bankverbindung und mehr
- **Filter-Funktionen**: Filtern nach Geschlecht und Altersbereich
- **Export-Formate**:
  - CSV (100 Personen auf einmal)
  - vCard (.vcf)
  - PDF
- **REST API**: JSON-Endpunkt für Programm-Integration
- **Progressive Web App (PWA)**: Installierbar als App
- **Dark Mode**: Umschaltbar zwischen hellem und dunklem Design
- **Docker-Support**: Einfaches Deployment mit Docker

## Generierte Datenfelder

- Name (ohne Titel)
- Geschlecht
- Geburtsdatum
- Alter (präzise berechnet)
- Adresse
- Telefonnummer
- E-Mail-Adresse
- Benutzername
- Beruf
- Firma
- IBAN
- BIC

## Installation

### Lokale Installation

1. Repository klonen:
```bash
git clone https://github.com/derdg1/personen-generator.git
cd personen-generator
```

2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. Anwendung starten:
```bash
python app.py
```

5. Browser öffnen: `http://localhost:5000`

### Docker

Mit Docker Compose:
```bash
docker-compose up -d
```

Oder mit Docker direkt:
```bash
docker build -t personen-generator .
docker run -p 5000:5000 personen-generator
```

Das vorgefertigte Image ist verfügbar unter:
```bash
docker pull ghcr.io/derdg1/personen-generator:latest
```

## API-Nutzung

### Einzelne Person generieren

```bash
curl http://localhost:5000/api/person
```

Antwort:
```json
{
  "Name": "Max Mustermann",
  "Geschlecht": "M",
  "Geburtsdatum": "1985-03-15",
  "Alter": 39,
  "Adresse": "Musterstraße 123, 12345 Berlin",
  "Telefon": "+49 30 12345678",
  "E-Mail": "max.mustermann@example.de",
  "Benutzername": "mmustermann",
  "Beruf": "Software-Entwickler",
  "Firma": "Musterfirma GmbH",
  "IBAN": "DE89370400440532013000",
  "BIC": "COBADEFFXXX"
}
```

### Gefilterte Person

```bash
curl "http://localhost:5000/filter?geschlecht=F&min=25&max=40"
```

## Technologie-Stack

- **Backend**: Python 3.11, Flask
- **Datengenerierung**: Faker (deutsche Lokalisierung)
- **PDF-Export**: ReportLab
- **Frontend**: Vanilla JavaScript, CSS Custom Properties
- **Containerisierung**: Docker

## Entwicklung

### Projektstruktur

```
personen-generator/
├── app.py                 # Flask-Anwendung
├── requirements.txt       # Python-Abhängigkeiten
├── Dockerfile            # Docker-Build-Konfiguration
├── docker-compose.yml    # Docker-Compose-Setup
├── .dockerignore         # Docker-Ignore-Regeln
├── .gitignore           # Git-Ignore-Regeln
├── templates/
│   └── index.html       # HTML-Template
└── static/
    ├── manifest.json    # PWA-Manifest
    ├── sw.js           # Service Worker
    ├── icon-192.png    # App-Icon 192x192
    └── icon-512.png    # App-Icon 512x512
```

### Code-Qualität

Die Anwendung:
- Filtert automatisch Namen mit akademischen Titeln aus
- Berechnet das Alter präzise unter Berücksichtigung des aktuellen Datums
- Verwendet deutsche Lokalisierung für realistische Daten
- Läuft produktionsbereit ohne Debug-Modus

## Lizenz

MIT License

## Hinweise

Diese Anwendung generiert **ausschließlich fiktive Daten** und sollte nur für Test- und Entwicklungszwecke verwendet werden. Die generierten Daten sind nicht echt und haben keine Verbindung zu realen Personen.
