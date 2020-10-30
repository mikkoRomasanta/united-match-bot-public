import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
SOURCE_PATH = os.getenv('SOURCE_PATH')
data_folder = Path(SOURCE_PATH)
