# Mini CRM

[![CI](https://github.com/akashb-jav/mini-crm-api/actions/workflows/ci.yml/badge.svg)](https://github.com/akashb-jav/mini-crm-api/actions/workflows/ci.yml)

A small API that records customer enquiries so a team can follow up.
Built with Python, FastAPI and SQLite.

## Run it

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs

## Endpoints

- GET / : health check
- POST /enquiries : create an enquiry
- GET /enquiries : list all enquiries
- GET /enquiries/{id} : get one enquiry
- PATCH /enquiries/{id}/status : change an enquiry's status
