# hubspot-api-etl

## What is HubSpot?
HubSpot is a CRM (Customer Relationship Management) platform used by businesses to manage sales, marketing, and customer support. It offers a REST API to retrieve and manage data such as contacts, deals, and companies.

## Overview
This is a production-style ETL that extracts **Contacts** and **Deals** from the HubSpot CRM v3 API, transforms the JSON into tabular form, and loads the data into **PostgreSQL** (with idempotent upsert) and/or **AWS S3** (as Parquet files). It supports pagination, rate-limit handling (429), and can be scheduled via GitHub Actions.

## Project Structure
```
hubspot-api-etl/
├── src/
│   ├── hubspot_client.py
│   ├── extract.py
│   ├── transform.py
│   ├── load_postgres.py
│   ├── load_s3.py
│   ├── utils.py
│   └── __init__.py
├── configs/objects.yml
├── sql/schema.sql
├── tests/test_transform.py
├── .github/workflows/etl.yml
├── .env.example
├── requirements.txt
└── .gitignore
```

## Quickstart
1. Create a **HubSpot Private App token** in your HubSpot portal.
2. Copy `.env.example` to `.env` and fill in the values.
3. (Optional) Create the database tables using `sql/schema.sql`.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the pipeline:
   ```bash
   python -m src.extract
   ```

## Notes
- Do not commit real tokens to GitHub. Use `.env` locally and GitHub Actions secrets in CI.
