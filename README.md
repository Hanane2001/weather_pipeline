# 🌤️ Weather Pipeline — Pipeline de données météo pour l'aide à la décision

Pipeline ETL complet qui récupère les prévisions météo des villes marocaines, calcule un score de risque pour chaque jour, stocke les données dans PostgreSQL et affiche un dashboard interactif.

---

## 📋 Table des matières

- [Contexte](#contexte)
- [Objectifs](#objectifs)
- [Sources de données](#sources-de-données)
- [Architecture du pipeline](#architecture-du-pipeline)
- [Schéma du Data Warehouse](#schéma-du-data-warehouse)
- [Structure du projet](#structure-du-projet)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Exécution du projet](#exécution-du-projet)
- [Airflow](#airflow)
- [Dashboard Streamlit](#dashboard-streamlit)
- [Requêtes SQL d'analyse](#requêtes-sql-danalyse)
- [Risk Score](#risk-score)
- [Diagrammes UML](#diagrammes-uml)

---

## Contexte

Une entreprise de livraison et de logistique opère dans plusieurs villes marocaines. Les conditions météorologiques (fortes pluies, vents violents, températures extrêmes) peuvent impacter ses opérations.

Ce projet met en place une solution permettant de :

- Récupérer les prévisions météo des prochains jours.
- Identifier les périodes et les villes à risque.
- Aider les responsables à anticiper les perturbations.
- Adapter l'organisation des livraisons.

---

## Objectifs

Répondre à la question métier :

> **Quelles villes et quelles périodes présentent le plus grand risque météorologique dans les prochains jours ?**

Le résultat doit permettre à un responsable opérationnel de :

- Comparer les conditions météo entre les villes.
- Identifier les périodes défavorables.
- Anticiper les risques pour les livraisons.
- Adapter l'organisation des opérations.

---

## Sources de données

### 1. SimpleMaps — Villes marocaines

- **URL** : https://simplemaps.com/data/ma-cities
- **Format** : CSV
- **Contenu** : nom de la ville, latitude, longitude, région, population.

### 2. Open-Meteo — Prévisions météo

- **URL** : https://api.open-meteo.com/v1/forecast
- **Format** : JSON
- **Variables récupérées** :
  - Maximum Temperature
  - Minimum Temperature
  - Precipitation Sum
  - Precipitation Probability Max
  - Maximum Wind Speed
  - Maximum Wind Gusts
  - Weather Code

**Paramètres utilisés** : `timezone=auto`, `forecast_days=7`

---

## Architecture du pipeline

Le pipeline suit une architecture **Bronze → Silver → Gold** :

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   BRONZE     │ ──► │   SILVER     │ ──► │    GOLD      │
│  Données     │     │  Données     │     │  Données     │
│  brutes      │     │  nettoyées   │     │  enrichies   │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  cities_raw.csv      weather_clean.csv   weather_features.csv
  weather_api.json
```

### 🥉 Bronze — Extraction

- Téléchargement du CSV des villes depuis SimpleMaps.
- Appel de l'API Open-Meteo pour chaque ville.
- Stockage brut dans `data/bronze/`.
- **Les données Bronze ne sont jamais modifiées.**

### 🥈 Silver — Nettoyage

- Standardisation des types et des dates.
- Suppression des doublons.
- Contrôle de cohérence (température min ≤ max, probabilité entre 0 et 100).
- Jointure entre les villes et les données météo.
- Résultat stocké dans `data/silver/`.

### 🥇 Gold — Feature Engineering

- Création des catégories (température, précipitations, vent).
- Calcul du **Risk Score** entre 0 et 100.
- Classification en Low / Medium / High.
- Résultat stocké dans `data/gold/`.

---

## Schéma du Data Warehouse

Trois tables principales reliées entre elles :

```
┌──────────────────┐
│      cities      │
├──────────────────┤
│ PK city_id       │
│    city          │
│    lat           │
│    lng           │
│    country       │
│    iso2          │
│    admin_name    │
│    capital       │
│    population    │
│    pop_proper    │
└────────┬─────────┘
         │ 1
         │
         │ N
┌────────▼─────────┐
│     weather      │
├──────────────────┤
│ PK weather_id    │
│ FK city_id       │
│    time          │
│    weather_code  │
│    temp_max      │
│    temp_min      │
│    prec_sum      │
│    prec_prob_max │
│    wind_speed    │
│    wind_gusts    │
└────────┬─────────┘
         │ 1
         │
         │ 1
┌────────▼──────────────┐
│   weather_features    │
├───────────────────────┤
│ PK feature_id         │
│ FK weather_id         │
│    temp_category      │
│    prec_category      │
│    wind_category      │
│    risk_temp          │
│    risk_prec          │
│    risk_wind          │
│    risk_score         │
│    risk_level         │
└───────────────────────┘
```

### Contraintes d'intégrité

- `cities.city` : UNIQUE
- `weather(city_id, time)` : UNIQUE — évite les doublons
- `weather_features.weather_id` : UNIQUE — 1 feature par prévision

---

## Structure du projet

```
weather-pipeline/
├── extraction/
│   ├── cities.py       # Téléchargement SimpleMaps
│   └── weather.py      # Appels API Open-Meteo
├── transformation/
│   ├── cleaning.py                # Nettoyage Silver
│   └── features.py             # Feature Engineering Gold
├── load/
│   └── postgres.py             # Connexion PostgreSQL
├── dashboard/
│   ├── app.py                  # Interface Streamlit
│   └── statistique.py          # Fonctions d'analyse
├── dags/
│   └── weather_pipeline.py          # DAG Airflow
├── sql/
│   ├── schema.sql              # Création des tables
│   └── analysis.sql    # Requêtes SQL métier
├── data/
│   ├── bronze/                 # Données brutes
│   ├── silver/                 # Données nettoyées
│   └── gold/                   # Données enrichies
├── UML/
│   ├── classe
│   |__ use_case
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Technologies utilisées

| Catégorie | Technologie |

| Langage | Python 3.14.3 |
| Manipulation de données | pandas, numpy |
| Appels API | requests |
| Base de données | PostgreSQL 17 |
| Connecteur PostgreSQL | psycopg2-binary |
| Orchestration | Apache Airflow 2.9 |
| Dashboard | Streamlit |
| Carte | Folium, streamlit-folium |
| Conteneurisation | Docker, Docker Compose |
| Configuration | python-dotenv |

---

## Installation

### Prérequis

- Python 3.14.3 ou plus
- Docker et Docker Compose
- Git

### Étapes

**1. Cloner le dépôt**

```bash
git clone https://github.com/ton-utilisateur/weather-pipeline.git
cd weather-pipeline
```

**2. Créer un environnement virtuel**

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate

# Linux / Mac
python3 -m venv .venv
source .venv/bin/activate
```

**3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**4. Créer le fichier `.env`**

Copie `.env.example` en `.env` et remplis les valeurs :

```env
DB_HOST=localhost
DB_PORT=....
DB_NAME=....
DB_USER=....
DB_PASSWORD=....
```

---

## Exécution du projet

### En local

**Étape 1 : Extraction Bronze**

```bash
python extraction/cities.py
python extraction/weather.py
```

**Étape 2 : Transformation Silver**

```bash
python transformation/cleaning.py
```

**Étape 3 : Feature Engineering Gold**

```bash
python transformation/features.py
```

**Étape 4 : Chargement PostgreSQL**

```bash
python load/postgres.py
```

**Étape 5 : Lancer le dashboard**

```bash
streamlit run dashboard/app.py
```

---

## Airflow

### DAG principal

Le DAG `weather_pipeline` orchestre les 5 étapes du pipeline :

```
cities ──► weather ──► cleaning ──► features ──► postgres
```

### Configuration

| Paramètre | Valeur |
|---|---|
| `dag_id` | weather_pipeline |
| `schedule` | `0 6 * * *` (tous les jours à 6h) |
| `retries` | 3 |
| `retry_delay` | 2 minutes |
| `catchup` | False |

### Accès

- URL : http://localhost:8080
- Identifiants : `admin` / `admin`
- Activer le DAG depuis l'interface.

---

## Dashboard Streamlit

### Fonctionnalités

Le dashboard permet de répondre à la question :

> **Où et quand faut-il être particulièrement vigilant dans les prochains jours ?**

### KPI affichés

| KPI | Description |

| Nombre de villes | Nombre de villes sélectionnées |
| Température max | Température maximale sur la période |
| Précipitations max | Précipitations maximales |
| Périodes à risque | Nombre de jours Medium ou High |
| Ville la plus risquée | Ville avec le score le plus élevé |

### Filtres

- Filtre par ville (multiselect)
- Filtre par date (plage de dates)
- Filtre par niveau de risque (Low / Medium / High)

### Visualisations

- Carte des villes avec points colorés par niveau de risque.
- Tableau des risques par ville.
- Graphique de température par ville.
- Graphique de précipitations par ville.

---

## Requêtes SQL d'analyse

Cinq requêtes métier disponibles dans `sql/analysis_queries.sql` :

**1. Villes avec les températures les plus élevées**
**2. Villes avec les plus fortes précipitations**
**3. Villes avec le risque moyen le plus élevé**
**4. Périodes avec le risque maximal**
**5. Pour chaque ville, la date du plus grand risque (sous-requête)**

---

## Risk Score

Le score de risque est compris entre **0 et 100**.

### Méthode de calcul

Trois sous-risques (0 à 3 chacun) sont additionnés puis ramenés sur 100.

| Composante | Variable | Seuils | Risque |
| Température | `temperature_2m_max` | > 30°C / > 35°C / > 40°C | 1 / 2 / 3 |
| Précipitations | `precipitation_sum` | > 0 / > 5 / > 20 mm | 1 / 2 / 3 |
| Vent | `wind_gusts_10m_max` | > 30 / > 50 / > 70 km/h | 1 / 2 / 3 |

**Formule** :

```
risk_score = ((risk_temp + risk_prec + risk_wind) / 9) * 100
```

### Classification

| Score | Niveau | Couleur |
|---|---|---|
| 0 – 33 | Low | 🟢 Vert |
| 34 – 66 | Medium | 🟠 Orange |
| 67 – 100 | High | 🔴 Rouge |

### Justification

- **Température** : impact sur les denrées périssables et le confort des livreurs.
- **Précipitations** : risque routier majeur (inondations, routes coupées).
- **Vent** : dangereux pour les livraisons à 2-roues, retards possibles.

---

## Diagrammes UML

### Diagramme de classes

Trois classes principales :

- **City** : villes marocaines avec coordonnées.
- **Weather** : prévisions journalières.
- **WeatherFeature** : indicateurs et score de risque.

Relations :

- `City (1) ── (0..*) Weather` : une ville a plusieurs prévisions.
- `Weather (1) ── (1) WeatherFeature` : une prévision a une feature.

### Diagramme de cas d'utilisation

Trois acteurs :

- **User** : consulte le dashboard et applique des filtres.
- **External (Open-Meteo API)** : fournit les données Bronze.
- **System (Airflow)** : déclenche le pipeline quotidien.

Voir les fichiers dans le dossier `UML/`.