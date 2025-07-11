import requests
from bs4 import BeautifulSoup
import json
import time
import os
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NBAScraper:
    def __init__(self, data_dir: str = "data/nba"):
        self.data_dir = data_dir
        self.base_url = "https://www.basketball-reference.com"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36", 
            "X-Amzn-Trace-Id": "Root=1-68706d95-7bb7de607d08b13b69ebaeba"
        })

        # Create data directories
        os.makedirs(f"{data_dir}/players", exist_ok=True)
        os.makedirs(f"{data_dir}/teams", exist_ok=True)
        os.makedirs(f"{data_dir}/games", exist_ok=True)
        os.makedirs(f"{data_dir}/news", exist_ok=True)

    def scrape_all_players(self, start_year: int=2014, end_year: int=2025) -> List[Dict]:
        """Scrape comprehensive player data for last decade"""
        all_players = [] # start with empty list

        for year in range(start_year, end_year + 1):
            logger.info(f"Scrapping players for {year} season...")
            season_players = self._scrape_season_players(year) # calling function
            all_players.extend(season_players) # add to list
            time.sleep(2) # Be respectful to the server

        # Remove duplicates and save
        unique_players = {p['name']: p for p in all_players}.values() 
        self._save_json(list(unique_players), "players/all_players.json")
        return list(unique_players)
    
    def _scrape_season_players(self, year: int) -> List[Dict]:
        """Scrape all players for a specific season"""
        url = f"{self.base_url}/leagues/NBA_{year}_per_game.html"

        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            players = []
            table = soup.find("table", {"id": "per_game_stats"})

            if not table:
                logger.warning(f"No per game stats table found for {year}")
                return []
            
            for row in table.find("tbody").find_all("tr"):
                if row.get("class") and "thead" in row.get("class"):
                    continue
                
                cells = row.find_all("td")
                if len(cells) < 10:
                    continue
                
                player_data = {
                    'name': cells[0].text.strip(),
                    'position': cells[1].text.strip(),
                    'age': cells[2].text.strip(),
                    'team': cells[3].text.strip(),
                    'games_played': cells[4].text.strip(),
                    'minutes_per_game': cells[7].text.strip(),
                    'points_per_game': cells[28].text.strip(),
                    'rebounds_per_game': cells[22].text.strip(),
                    'assists_per_game': cells[23].text.strip(),
                    'season': year,
                    'scraped_at': datetime.now().isoformat()
                }

                # Get detailed player bio
                player_link = cells[0].find("a")
                if player_link:
                    player_data["bio"] = self._scrape_player_bio(player_link["href"])
                    time.sleep(1) # rate limiting

                players.append(player_data)

            logger.info(f"Scraped {len(players)} players for {year}")
            return players

        except Exception as e:
            logger.error(f"Error scraping {year}: {str(e)}")
            return []
        
    def _scrape_player_bio(self, player_path: str) -> Dict:
        """Scrape etailed player biography and career highlights"""
        url = f"{self.base_url}{player_path}"

        try:
            response = self.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            bio_data = {}

            # Get basic info
            info_box = soup.find("div", {"itemtype": "https://schema.org/Person"})
            if info_box:
                for p in info_box.find_all("p"):
                    text = p.text.strip()
                    if "Born" in text:
                        bio_data["birth_info"] = text
                    elif "College" in text:
                        bio_data["college"] = text
                    elif "Draft" in text:
                        bio_data["draft_info"] = text
            
            # Get career highlights
            highlights = []
            for strong in soup.find_all("strong"):
                if any(keyword in strong.text.lower() for keyword in
                       ["all-star", "champion", "mvp", "rookie", "finals"]):
                    highlights.append(strong.parent.text.strip())

            bio_data["career_highlights"] = highlights

            # Get injury history from any mentions
            injury_keywords = ["injury", "injured", "surgery", "rehab", "recovery"]
            injury_mentions = []
            for p in soup.find_all("p"):
                text = p.text.lower()
                if any(keyword in text for keyword in injury_keywords):
                    injury_mentions.append(p.text.strip())

            bio_data["injury_history"] = injury_mentions[:5] # Limit to 5 mentions

            return bio_data
        
        except Exception as e:
            logger.error(f"Error scraping bio: {str(e)}")
            return {}

    def scrape_recent_news(self, days_back: int=30) -> List[Dict]:
        """Scrape recent NBA news and headlines"""
        # This would integrate with ESPN, NBA.com, or other news sources
        # For now, we'll create a placeholder structure

        news_articles = []
        
        # ESPN NBA news (example)
        try:
            espn_url = "https://www.espn.com/nba/news"
            response = self.session.get(espn_url)
            soup = BeautifulSoup(response.content, "html.parser")

            for articles in soup.find_all("article")[:20]: # Get top 20 articles
                headline_elem = article.find("h1") or article.find("h2")
                if headline_elem:
                    news_articles.append({
                        "headline": headline_elem.text.strip(),
                        'source': 'ESPN',
                        'scraped_at': datetime.now().isoformat(),
                        'category': 'news'
                    })

        except Exception as e:
            logger.error(f"Error scrapping news: {str(e)}")

        self._save_json(news_articles, "news/recent_headlines.json")
        return news_articles
    
    def _save_json(self, data: any, filename: str):
        """Save data to JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved data to {filename}")

if __name__ == "__main__":
    scraper = NBAScraper()

    # Scraper player data from the last decade
    print("🏀 Starting NBA data collection...")

    players = scraper.scrape_all_players(2020, 2025) # Start with recent
    print(f"✅ Collected data for {len(players)} players")

    news = scraper.scrape_recent_news()
    print(f"✅ Collected {len(news)} news articles")
    
    print("🎯 NBA data collection complete!")


