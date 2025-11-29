import os, sys
import json
from typing import List
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from logging_config import setup_logging

setup_logging()

def load_stored_urls():
    logging.info("Saving new URLs")
    
    if not os.path.exists("storage/stored_urls.json"):
        return []
    
    with open("storage/stored_urls.json", "r") as f:
        return json.load(f)

def save_stored_urls(new_urls: List[str]):
    logging.info("Saving new urls")

    existing_urls = load_stored_urls()

    combined_urls = list(set(existing_urls + new_urls))

    with open("storage/stored_urls.json", "w") as f:
        json.dump(combined_urls, f, indent=2)
    

