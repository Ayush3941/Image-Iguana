# main.py

import os
from app import create_app, db
from config import DevelopmentConfig
from dotenv import load_dotenv

load_dotenv()
print("Loaded DATABASE_URL:", os.getenv("DATABASE_URL"))

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(debug=True)
