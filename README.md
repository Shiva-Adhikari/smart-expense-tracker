
# Smart Expense Tracker

> A comprehensive expense tracking REST API built to help you take control of your finances with AI-powered insights.

## Description

A full-featured expense tracking application built with FastAPI, SQLAlchemy and PostgreSQL. Track your expenses, manage budgets, monitor income, and gain valuable insights into your financial habits through automated reports and AI-powered categorization.

## Features

### Authentication & Security

- User authentication with JWT tokens
- Bcrypt password hashing
- Rate limiting to prevent abuse

### Expense Management

- Complete CRUD operations for expenses
- Category-based organization
- File upload support for receipts
- Search and filtering capabilities

### Budget & Income Tracking

- Set monthly budgets per category
- Real-time budget status monitoring
- Income tracking from multiple sources
- Spending limit management

### AI-Powered Insights

- Smart expense categorization using machine learning
- Anomaly detection for unusual transactions
- Spending predictions (daily, weekly, monthly)

### Reports & Analytics

- Authomated monthly financial reports
- Category-wise expense breakdown
- Trend analysis and visualizations
- Export data to CSV, Excel and PDF formats

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL
- **Frontend:** React
- **ML:** scikit-learn (TF-IDF, Logistic Regression)

## Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL 15+
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shiva-adhikari/smart-expense-tracker.git
cd smart-expense-tracker
```

### 2. Backend Setup

```bash
cd backend

# Create virtual envicornment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### using sync,
```bash
uv sync
```

### 3. Database Setup

Install PostgreSQL locally and creae a database named `smart_expense_tracker` and username should be `postgres`

## Configuration

Create a `.env` file in the `backend/` directory:
```env
# Database
DATABASE_URL = 'postgresql://username:password@localhost:5432/database_username'

# Database engine Debug
DEBUG = False

# Logging level (logging)
DEBUG_LEVEL = DEBUG
```

## Usage

### Start the Backend Server
#### with uv,
```shell
cd backend
uv run python -m src.main:app --reload
```

#### without uv,
```shell
cd backend
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

Access API Documentation
Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

## Testing

### with uv,
```shell
cd backend

#Run all tests
# with uv
uv run python -m pytest

# Run with coverage
uv run python -m pytest --cov=app

# Run specific test file
uv run python -m pytest tests/api/test_authentication.py
```

### without uv,
```shell
cd backend

#Run all tests
# without uv
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/api/test_authentication.py
```

## Commands

| Command                                 | Description                   |
| --------------------------------------- | ----------------------------- |
| `uvicorn app.main:app --reload`         | Start backend with hot reload |
| `uv run python -m pytest location/path` | Run all tests                 |
| `pip freeze > requirements.txt`         | Update dependencies file      |

## Roadmap

- [ ] Dashboard with charts
- [ ] Receipt OCR integration
- [ ] Mobile responsive design
- [ ] Multi-currency support
- [ ] Recurring expense automation

## License

 This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- [scikit-learn](https://scikit-learn.org/) - Machine learning library

Built with ❤️ using FastAPI, React, and ML integration for personal finance management.
