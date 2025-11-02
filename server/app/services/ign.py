import requests
from sqlmodel import Session
from typing import Dict, Any, List
import xml.etree.ElementTree as ET
from datetime import datetime

from core.logger import logger
from core.categories import ServiceCategory
from services.services_classes import (
    Service as ServiceClass,
    Action,
    get_component,
)
from services.area_api import AreaApi
from models import AreaAction


class IGNApiError(Exception):
    """IGN API-specific errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class IGNApi(AreaApi):
    """IGN API wrapper."""

    def __init__(self):
        super().__init__(IGNApiError)
        self.base_url = "https://www.ign.com"

    def get_articles(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get latest articles from IGN RSS feed."""
        try:
            url = f"{self.base_url}/rss/articles"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise IGNApiError(f"Failed to fetch articles: {response.status_code}")

            root = ET.fromstring(response.content)
            articles = []

            for item in root.findall(".//item")[:count]:
                article = {
                    "title": item.find("title").text
                    if item.find("title") is not None
                    else "",
                    "link": item.find("link").text
                    if item.find("link") is not None
                    else "",
                    "description": item.find("description").text
                    if item.find("description") is not None
                    else "",
                    "pub_date": item.find("pubDate").text
                    if item.find("pubDate") is not None
                    else "",
                    "guid": item.find("guid").text
                    if item.find("guid") is not None
                    else "",
                }
                articles.append(article)

            return articles
        except ET.ParseError as e:
            raise IGNApiError(f"Failed to parse RSS feed: {str(e)}")
        except Exception as e:
            raise IGNApiError(f"Error fetching articles: {str(e)}")

    def get_reviews(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get latest reviews from IGN RSS feed."""
        try:
            url = f"{self.base_url}/rss/reviews"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise IGNApiError(f"Failed to fetch reviews: {response.status_code}")

            root = ET.fromstring(response.content)
            reviews = []

            for item in root.findall(".//item")[:count]:
                review = {
                    "title": item.find("title").text
                    if item.find("title") is not None
                    else "",
                    "link": item.find("link").text
                    if item.find("link") is not None
                    else "",
                    "description": item.find("description").text
                    if item.find("description") is not None
                    else "",
                    "pub_date": item.find("pubDate").text
                    if item.find("pubDate") is not None
                    else "",
                    "guid": item.find("guid").text
                    if item.find("guid") is not None
                    else "",
                }
                reviews.append(review)

            return reviews
        except ET.ParseError as e:
            raise IGNApiError(f"Failed to parse RSS feed: {str(e)}")
        except Exception as e:
            raise IGNApiError(f"Error fetching reviews: {str(e)}")

    def get_videos(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get latest videos from IGN RSS feed."""
        try:
            url = f"{self.base_url}/rss/videos"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise IGNApiError(f"Failed to fetch videos: {response.status_code}")

            root = ET.fromstring(response.content)
            videos = []

            for item in root.findall(".//item")[:count]:
                video = {
                    "title": item.find("title").text
                    if item.find("title") is not None
                    else "",
                    "link": item.find("link").text
                    if item.find("link") is not None
                    else "",
                    "description": item.find("description").text
                    if item.find("description") is not None
                    else "",
                    "pub_date": item.find("pubDate").text
                    if item.find("pubDate") is not None
                    else "",
                    "guid": item.find("guid").text
                    if item.find("guid") is not None
                    else "",
                }
                videos.append(video)

            return videos
        except ET.ParseError as e:
            raise IGNApiError(f"Failed to parse RSS feed: {str(e)}")
        except Exception as e:
            raise IGNApiError(f"Error fetching videos: {str(e)}")

    def get_news(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get latest news from IGN RSS feed."""
        try:
            url = f"{self.base_url}/rss/news"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise IGNApiError(f"Failed to fetch news: {response.status_code}")

            root = ET.fromstring(response.content)
            news_items = []

            for item in root.findall(".//item")[:count]:
                news = {
                    "title": item.find("title").text
                    if item.find("title") is not None
                    else "",
                    "link": item.find("link").text
                    if item.find("link") is not None
                    else "",
                    "description": item.find("description").text
                    if item.find("description") is not None
                    else "",
                    "pub_date": item.find("pubDate").text
                    if item.find("pubDate") is not None
                    else "",
                    "guid": item.find("guid").text
                    if item.find("guid") is not None
                    else "",
                }
                news_items.append(news)

            return news_items
        except ET.ParseError as e:
            raise IGNApiError(f"Failed to parse RSS feed: {str(e)}")
        except Exception as e:
            raise IGNApiError(f"Error fetching news: {str(e)}")


ign_api = IGNApi()


class IGN(ServiceClass):
    """IGN gaming news and reviews service."""

    def __init__(self) -> None:
        super().__init__(
            "IGN gaming news, reviews and videos",
            ServiceCategory.GAMING,
            "#D72121",
            "/images/IGN_logo.webp",
            False,
        )

    class new_article(Action):
        """Triggered when a new article is published on IGN."""

        service: "IGN"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Keywords",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__(
                "Triggered when a new article is published (optional: filter by keywords)",
                config_schema,
                "*/10 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                keywords_input = get_component(area_action.config, "Keywords", "values")
                keywords = (
                    [k.strip().lower() for k in keywords_input.split(",")]
                    if keywords_input
                    else []
                )

                articles = ign_api.get_articles(count=5)

                if not articles:
                    return False

                latest_article = articles[0]

                if not area_action.last_state or "guid" not in area_action.last_state:
                    area_action.last_state = {"guid": latest_article["guid"]}
                    session.add(area_action)
                    session.commit()
                    return False

                if latest_article["guid"] == area_action.last_state.get("guid"):
                    return False

                if keywords:
                    title_lower = latest_article["title"].lower()
                    description_lower = latest_article["description"].lower()

                    if not any(
                        keyword in title_lower or keyword in description_lower
                        for keyword in keywords
                    ):
                        area_action.last_state = {"guid": latest_article["guid"]}
                        session.add(area_action)
                        session.commit()
                        return False

                area_action.last_state = {"guid": latest_article["guid"]}
                session.add(area_action)
                session.commit()
                return True

            except IGNApiError as e:
                logger.error(f"IGN new_article check error: {e.message}")
                return False
            except Exception as e:
                logger.error(f"IGN new_article unexpected error: {str(e)}")
                return False

    class new_review(Action):
        """Triggered when a new review is published on IGN."""

        service: "IGN"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Keywords",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__(
                "Triggered when a new game review is published (optional: filter by keywords)",
                config_schema,
                "*/15 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                keywords_input = get_component(area_action.config, "Keywords", "values")
                keywords = (
                    [k.strip().lower() for k in keywords_input.split(",")]
                    if keywords_input
                    else []
                )

                reviews = ign_api.get_reviews(count=5)

                if not reviews:
                    return False

                latest_review = reviews[0]

                if not area_action.last_state or "guid" not in area_action.last_state:
                    area_action.last_state = {"guid": latest_review["guid"]}
                    session.add(area_action)
                    session.commit()
                    return False

                if latest_review["guid"] == area_action.last_state.get("guid"):
                    return False

                if keywords:
                    title_lower = latest_review["title"].lower()
                    description_lower = latest_review["description"].lower()

                    if not any(
                        keyword in title_lower or keyword in description_lower
                        for keyword in keywords
                    ):
                        area_action.last_state = {"guid": latest_review["guid"]}
                        session.add(area_action)
                        session.commit()
                        return False

                area_action.last_state = {"guid": latest_review["guid"]}
                session.add(area_action)
                session.commit()
                return True

            except IGNApiError as e:
                logger.error(f"IGN new_review check error: {e.message}")
                return False
            except Exception as e:
                logger.error(f"IGN new_review unexpected error: {str(e)}")
                return False

    class new_video(Action):
        """Triggered when a new video is published on IGN."""

        service: "IGN"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Keywords",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__(
                "Triggered when a new video is published (optional: filter by keywords)",
                config_schema,
                "*/10 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                keywords_input = get_component(area_action.config, "Keywords", "values")
                keywords = (
                    [k.strip().lower() for k in keywords_input.split(",")]
                    if keywords_input
                    else []
                )

                videos = ign_api.get_videos(count=5)

                if not videos:
                    return False

                latest_video = videos[0]

                if not area_action.last_state or "guid" not in area_action.last_state:
                    area_action.last_state = {"guid": latest_video["guid"]}
                    session.add(area_action)
                    session.commit()
                    return False

                if latest_video["guid"] == area_action.last_state.get("guid"):
                    return False

                if keywords:
                    title_lower = latest_video["title"].lower()
                    description_lower = latest_video["description"].lower()

                    if not any(
                        keyword in title_lower or keyword in description_lower
                        for keyword in keywords
                    ):
                        area_action.last_state = {"guid": latest_video["guid"]}
                        session.add(area_action)
                        session.commit()
                        return False

                area_action.last_state = {"guid": latest_video["guid"]}
                session.add(area_action)
                session.commit()
                return True

            except IGNApiError as e:
                logger.error(f"IGN new_video check error: {e.message}")
                return False
            except Exception as e:
                logger.error(f"IGN new_video unexpected error: {str(e)}")
                return False

    class new_news(Action):
        """Triggered when a new news item is published on IGN."""

        service: "IGN"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Keywords",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__(
                "Triggered when a new news item is published (optional: filter by keywords)",
                config_schema,
                "*/10 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                keywords_input = get_component(area_action.config, "Keywords", "values")
                keywords = (
                    [k.strip().lower() for k in keywords_input.split(",")]
                    if keywords_input
                    else []
                )

                news_items = ign_api.get_news(count=5)

                if not news_items:
                    return False

                latest_news = news_items[0]

                if not area_action.last_state or "guid" not in area_action.last_state:
                    area_action.last_state = {"guid": latest_news["guid"]}
                    session.add(area_action)
                    session.commit()
                    return False

                if latest_news["guid"] == area_action.last_state.get("guid"):
                    return False

                if keywords:
                    title_lower = latest_news["title"].lower()
                    description_lower = latest_news["description"].lower()

                    if not any(
                        keyword in title_lower or keyword in description_lower
                        for keyword in keywords
                    ):
                        area_action.last_state = {"guid": latest_news["guid"]}
                        session.add(area_action)
                        session.commit()
                        return False

                area_action.last_state = {"guid": latest_news["guid"]}
                session.add(area_action)
                session.commit()
                return True

            except IGNApiError as e:
                logger.error(f"IGN new_news check error: {e.message}")
                return False
            except Exception as e:
                logger.error(f"IGN new_news unexpected error: {str(e)}")
                return False
