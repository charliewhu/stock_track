
# Production Tracker App

This app is a tracker for an imaginary commodity operations department to track production at various locations.

It aims to allow easy create, list, update and delete functionality for various fields, and show the trend in readily available graphs.

### Features

- FastApi CLUD endpoints
- Data persisted to a local SQLite database
- Streamlit UI
- Plotly charts
- API happy path tested (Pytest)


### Potential Enhancements

- Add Fields / Grades for another granularity
- Ability to filter charts by Field / Grade
- Authentication and authorization middleware
- Error handling for API endpoints
- Frontend error handling in Streamlit UI
- Additional UI filters
- Unit tests for Services
- End-to-end testing for UI interaction (Playwright etc)
- Decouple domain logic from database models if required later


## How to use

- Ensure docker is installed and running

```bash
docker compose up --build
```

- By default, the UI runs on http://localhost:8501
- The API runs on http://localhost:8000
