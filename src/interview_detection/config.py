import os

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
print("PROJECT_DIR:\t", PROJECT_DIR)

DATA_FOLDER = os.path.join(PROJECT_DIR, 'data')
MODELS_FOLDER = os.path.join(PROJECT_DIR, 'models')
LOGS_FOLDER = os.path.join(PROJECT_DIR, 'logs')
