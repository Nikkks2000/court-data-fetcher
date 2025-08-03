# court-data-fetcher
Court-Data Fetcher is a lightweight Flask-based web app
This is a Flask web application designed to scrape court data and store it in a local SQLite database.

Project Structure
court-data-fetcher/
app.py                -Main Flask 
scraper.py            -web scraping logic (currently placeholder)
templates/            -web interface
  index.html          -Homepage 
  result.html         -scraped or stored data
  error.html          -error messages
.env                  -Environment variables
requirements.txt      -Python dependencies


Setup and Installation
Clone the repository (or create the files manually):

git clone <your-repo-url>
cd court-data-fetcher

Create a Python Virtual Environment:
python3 -m venv venv

Activate the Virtual Environment:

Install Dependencies:
pip install -r requirements.txt
