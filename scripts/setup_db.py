from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


def set_connection():
    '''
    Sets up connection factory for database given by URL in the .env file.
    '''
    load_dotenv()
    db_url = os.getenv('DB_URL')
    engine = create_engine(db_url)

    return engine
