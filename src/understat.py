import re
import json
import random
import logging
import requests

import pandas as pd
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(levelname)-8s | %(name)-20s | %(message)s',
    level=logging.INFO
    )


def get_user_agent() -> str:
    user_agent_strings = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    ]
    return random.choice(user_agent_strings)


def get_soup(team: str, year: str) -> BeautifulSoup:
    headers = {}
    headers["UserAgent"] = get_user_agent()
    
    
    try:
        url = f'https://understat.com/team/{team}/{year}'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
    except Exception as e:
        logger.warning("No soup object or data found")
        logger.warning(e)
        print(e)
        return None
    
    scripts = soup.find_all('script')
    for script in scripts:
        if 'playersData' in script.text:
            data_script = script.text
            
            logger.debug("playersData found")
            
            json_data = re.search(r'playersData\s*=\s*JSON.parse\((.*)\)', data_script).group(1)
            json_data = json_data[1:-1]
            
            decoded_data = bytes(json_data, "utf-8").decode("unicode_escape")
            parsed_data = json.loads(decoded_data)

            df = pd.DataFrame(parsed_data)            
            return df
    return None
    
    
    

if __name__ == "__main__":
    data = get_soup(team="Inter", year="2023")