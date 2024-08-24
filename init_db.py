from app import create_app, db
from logger import logger

app = create_app()
with app.app_context():
    logger.info('Initializing database')
    db.create_all()
    logger.info('Database tables created successfully')