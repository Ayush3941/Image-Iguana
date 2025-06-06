# main.py

import os
from app import create_app, db
from app.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        os.makedirs('static', exist_ok=True)
        os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
