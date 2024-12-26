# Backend Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [Directory Structure](#directory-structure)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

---

## Project Overview
This backend project is built using **FastAPI**, designed to handle core functionalities such as user authentication, transaction management, and exchange rate operations. It includes robust APIs, secure password hashing, and token-based authentication.

---

## Features
- User authentication and authorization
- CRUD operations for transactions
- Real-time exchange rate management
- SQLite3 database integration
- Pydantic-based request/response validation
- Unit and integration tests

---

## Installation

### Prerequisites
- Python 3.9 or above
- Node.js (for managing `node_modules`)
- SQLite (pre-installed with Python)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd newbackend
   ```
2.Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3.Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install node.js:
   ```bash
   nstall Node.js dependencies (if applicable):
   ```

### Running the Application

```bash
uvicorn app.main:app --reload
```
   





