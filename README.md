# Code Challenge Generator

This is a web application that generates coding challenges (multiple-choice questions) using an AI model and allows users to test their knowledge.

## Features

*   Generate coding challenges using AI.
*   Multiple choice questions format.
*   User authentication.
*   View history of challenges.

## Technologies Used

*   **Frontend:** React, Vite, Clerk (for authentication)
*   **Backend:** Python, Flask, SQLAlchemy
*   **AI:** Gemini
*   **Database:** SQLite

## Getting Started

### Prerequisites

*   Node.js and npm
*   Python 3.12
*   `uv` for python package management

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jaz123-code/code_challenge_generator_by_jaz.git
    cd code_challenge_generator_by_jaz
    ```

2.  **Backend Setup:**
    ```bash
    cd backend
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    # Add your .env file with necessary API keys
    cd ..
    ```

3.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    # Add your .env file with necessary Clerk credentials
    cd ..
    ```

## Usage

1.  **Start the backend server:**
    ```bash
    cd backend
    source .venv/bin/activate
    python main.py
    ```

2.  **Start the frontend development server:**
    ```bash
    cd frontend
    npm run dev
    ```

Open your browser and navigate to the URL provided by Vite.
