from fastapi import FastAPI, HTTPException

from typing import List, Optional
from sqlite3 import Connection, Cursor
import sqlite3

import requests
# web scraper
from scraper import scraper

# Models
from model import ThemePredictor
# Initialise Model
ThemePredictor = ThemePredictor()

app = FastAPI()

DATABASE = "themes.db"

def init_db():
    """ 
    Method initilises a database with 3 columns
    1. ID
    2. URL
    3. Text Body
    4. Theme
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS themes (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            text_body TEXT NOT NULL,
            theme TEXT NOT NULL
        )
        """)

# Initialise database #
init_db()


@app.post("/extract-theme/")
async def extract_theme(url: str):
    """ 
    Method extracts text from url, predicts theme of the content and saves down the url, text and theme 
    into a sqlite database

    Args:
    - url: url of SEC filing
    # test_url = 'https://www.sec.gov/Archives/edgar/data/1267238/000126723822000006/aiz-20211231.htm'

    Returns: 
    - { url, theme}
    """

    try:
        # Scrape Text from URL
        text_body = scraper(url)

        # Predicts theme from text body
        theme = ThemePredictor.predict(text_body)

        # Saves into a sqlite database
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO themes (url, text_body, theme) VALUES (?, ?, ?)", (url, text_body, theme))
            conn.commit()

        return {"url": url, "theme": theme}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/get-predicted-themes/")
async def get_predicted_themes() -> list:
    """
    Retrieve a list of all extracted themes from the database.

    Returns:
    - A list of themes stored in the database.
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT theme FROM themes").fetchall()
        themes = [row[0] for row in rows]

    return themes

@app.get("/texts/{theme_name}/")
async def get_texts_by_theme(theme_name: str):
    """
    Retrieve a list of text associated with a specific theme.

    Args:
    - theme_name (str): The theme to filter by.

    Returns:
    - ThemeList: A list of text bodies associated with the specified theme.
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT url, text_body, theme FROM themes WHERE theme=?", (theme_name,)).fetchall()
        themes = [{"url": row[0], "text_body": row[1][0:150] + " ...", "theme": row[2]} for row in rows]
    return {"themes": themes}

    



