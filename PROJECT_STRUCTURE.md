# SmartFactory Monitor — Project Structure

```
smartfactory-monitor/
│
├── 📁 app/                          # Core FastAPI application
│   ├── __init__.py
│   ├── main.py                      # FastAPI entry point, app factory
│   ├── config.py                    # Settings via pydantic-settings
│   │
│   ├── 📁 api/                      # Route handlers (versioned)
│   │   ├── __init__.py
│   │   ├── 📁 v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py            # Aggregates all v1 routers
│   │   │   ├── sensors.py           # GET/POST /sensors endpoints
│   │   │   ├── anomalies.py         # GET /anomalies endpoints
│   │   │   └── alerts.py            # POST /alerts/trigger endpoint
│   │   └── websocket.py             # WebSocket real-time endpoint
│   │
│   ├── 📁 core/                     # App-wide utilities
│   │   ├── __init__.py
│   │   ├── database.py              # SQLAlchemy async engine + session
│   │   ├── redis.py                 # Redis connection pool
│   │   ├── security.py              # API key auth dependency
│   │   └── exceptions.py            # Custom HTTP exceptions
│   │
│   ├── 📁 models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── sensor.py                # SensorReading table
│   │   ├── anomaly.py               # Anomaly table
│   │   └── alert.py                 # Alert log table
│   │
│   ├── 📁 schemas/                  # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── sensor.py                # SensorReadingCreate, SensorReadingOut
│   │   ├── anomaly.py               # AnomalyOut, AnomalyFilter
│   │   └── alert.py                 # AlertCreate, AlertOut
│   │
│   ├── 📁 services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── sensor_service.py        # Save/query sensor readings
│   │   ├── anomaly_service.py       # Pandas-based anomaly detection
│   │   └── alert_service.py         # Telegram notification logic
│   │
│   └── 📁 tasks/                    # Celery async tasks
│       ├── __init__.py
│       ├── celery_app.py            # Celery factory + Redis broker config
│       ├── scraper_tasks.py         # Periodic web scraping tasks
│       └── detection_tasks.py       # Scheduled anomaly detection tasks
│
├── 📁 collectors/                   # Data collection modules
│   ├── __init__.py
│   ├── mqtt_listener.py             # paho-mqtt subscriber (IoT simulation)
│   ├── web_scraper.py               # Selenium/Playwright scraper
│   └── api_fetcher.py               # httpx async API client
│
├── 📁 tests/                        # Pytest test suite
│   ├── conftest.py                  # Fixtures: test DB, test client, mocks
│   ├── 📁 unit/
│   │   ├── test_anomaly_service.py  # Pure logic tests (Pandas)
│   │   ├── test_schemas.py          # Pydantic validation tests
│   │   └── test_sensor_service.py
│   └── 📁 integration/
│       ├── test_sensors_api.py      # Full HTTP tests with TestClient
│       ├── test_websocket.py        # WebSocket connection tests
│       └── test_tasks.py            # Celery task integration tests
│
├── 📁 alembic/                      # DB migrations
│   ├── env.py
│   ├── script.py.mako
│   └── 📁 versions/
│       └── 001_initial_schema.py
│
├── 📁 docker/                       # Docker configs
│   ├── Dockerfile                   # Multi-stage Python image
│   ├── Dockerfile.worker            # Celery worker image
│   └── nginx.conf                   # Reverse proxy config
│
├── 📁 .github/
│   └── 📁 workflows/
│       ├── ci.yml                   # Run tests on every PR
│       └── deploy.yml               # Deploy on merge to main
│
├── 📁 scripts/
│   ├── seed_db.py                   # Insert demo sensor data
│   └── simulate_mqtt.py             # Simulate IoT sensor stream
│
├── docker-compose.yml               # Full stack: API + Worker + DB + Redis
├── docker-compose.test.yml          # Isolated test environment
├── pyproject.toml                   # Dependencies (Poetry)
├── .env.example                     # Environment variable template
├── alembic.ini
└── README.md
```

## Tech stack summary

| Layer | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn |
| Data Validation | Pydantic v2 + pydantic-settings |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL |
| Cache / Broker | Redis |
| Task Queue | Celery |
| Data Processing | Pandas, NumPy |
| Web Scraping | Selenium, Playwright, httpx |
| IoT Protocol | paho-mqtt |
| Notifications | python-telegram-bot |
| Testing | Pytest, pytest-asyncio, httpx |
| DevOps | Docker, GitHub Actions, Grafana |
