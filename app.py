from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from dotenv import load_dotenv
import os
import time # For ethical scraping delays
from scraper import scrape_court_data # Assuming scraper.py has this function

load_dotenv() # Load environment variables from .env

app = Flask(__name__)
DATABASE = 'db.sqlite3'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name (e.g., row['column_name'])
    return conn

def init_db():
    """Initializes the database by creating the 'cases' table if it doesn't exist."""
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create a table for court cases
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_number TEXT NOT NULL UNIQUE,
                party_names TEXT,
                filing_date TEXT,
                status TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    """Renders the main page (index.html) for user input."""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    """
    Handles the scraping request.
    It retrieves the search term, calls the scraper, saves data to the database,
    and displays the results or an error.
    """
    search_term = request.form.get('search_term')
    if not search_term:
        return render_template('error.html', message="Search term is required.")

    try:
        # Call the scraper function to get data
        scraped_data = scrape_court_data(search_term)

        conn = get_db_connection()
        cursor = conn.cursor()
        for item in scraped_data:
            try:
                # Insert or ignore to prevent duplicate case numbers
                cursor.execute('''
                    INSERT OR IGNORE INTO cases (case_number, party_names, filing_date, status)
                    VALUES (?, ?, ?, ?)
                ''', (item.get('case_number'), item.get('party_names'), item.get('filing_date'), item.get('status')))
            except sqlite3.IntegrityError:
                # This block will be hit if INSERT OR IGNORE finds a duplicate and ignores it
                print(f"Duplicate case number skipped: {item.get('case_number')}")
            except Exception as e:
                print(f"Error inserting data for case {item.get('case_number')}: {e}")
        conn.commit()
        conn.close()

        return render_template('result.html', data=scraped_data, source="Scraped Data")
    except Exception as e:
        # Catch any exceptions during scraping or database operations
        return render_template('error.html', message=f"An error occurred during scraping: {e}")

@app.route('/view_data')
def view_data():
    """
    Retrieves all previously scraped data from the database
    and displays it on the result page.
    """
    conn = get_db_connection()
    # Fetch all cases, ordered by when they were scraped
    cases = conn.execute('SELECT * FROM cases ORDER BY scraped_at DESC').fetchall()
    conn.close()
    return render_template('result.html', data=cases, source="Database Records")

if __name__ == '__main__':
    # Initialize the database when the application starts
    init_db()
    # Run the Flask application in debug mode (for development)
    app.run(debug=True)
