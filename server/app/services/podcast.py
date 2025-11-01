"""Podcast RSS feed monitoring service.

Provides automation for monitoring podcast RSS feeds without OAuth requirements.
Allows users to track new episodes, keyword matches, and episode counts.
"""

from models import AreaAction, AreaReaction
from sqlmodel import Session
from services.services_classes import Service, Action, Reaction, get_component
from core.logger import logger
from core.categories import ServiceCategory
from typing import List, Dict, Any
import requests
import xml.etree.ElementTree as ET


class PodcastApiError(Exception):
    """Podcast API error exception."""

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


PRESET_PODCASTS = {
    "NPR News Now": "https://feeds.npr.org/500005/podcast.xml",
    "The Daily (NY Times)": "https://feeds.simplecast.com/54nAGcIl",
    "The Joe Rogan Experience": "https://feeds.megaphone.fm/ROOSTER7199250968",
    "Stuff You Should Know": "https://feeds.megaphone.fm/stuffyoushouldknow",
    "Crime Junkie": "https://feeds.simplecast.com/dHoohVNH",
    "Acquired": "https://feeds.transistor.fm/acquired",
    "Darknet Diaries": "https://feeds.megaphone.fm/darknetdiaries",
    "Lex Fridman Podcast": "https://lexfridman.com/feed/podcast/",
    "Huberman Lab": "https://feeds.simplecast.com/wjQvV1tl",
    "The Tim Ferriss Show": "https://feeds.acast.com/public/shows/the-tim-ferriss-show",
    "SmartLess": "https://feeds.megaphone.fm/smartless",
    "Call Her Daddy": "https://feeds.simplecast.com/GLQ8zCVt",
    "TED Talks Daily": "https://feeds.megaphone.fm/ROOSTER3920042267",
    "Armchair Expert with Dax Shepard": "https://feeds.simplecast.com/X4jjNfKj",
    "Conan O'Brien Needs a Friend": "https://feeds.megaphone.fm/conan-OBrien-needs-a-friend",
    "Planet Money": "https://feeds.npr.org/510318/podcast.xml",
    "Science Vs": "https://feeds.megaphone.fm/sciencevs",
    "This American Life": "https://feeds.thisamericanlife.org/talpodcast",
    "Serial": "https://feeds.megaphone.fm/ARNODT6883435471",
    "My Favorite Murder": "https://feeds.simplecast.com/qm_9xx0g",
    "Custom URL": "",
}


def _get_podcast_selection_fields() -> List[Dict[str, Any]]:
    """Generate standard podcast selection config fields."""
    return [
        {
            "name": "Podcast Selection",
            "type": "select",
            "values": list(PRESET_PODCASTS.keys()),
        },
        {"name": "Custom RSS Feed URL", "type": "input", "values": []},
    ]


def _resolve_rss_url(config: Any) -> str:
    """Resolve RSS URL from config (handles preset selection or custom URL)."""
    preset_name = get_component(config, "Podcast Selection", "values")  # type: ignore
    custom_url = get_component(config, "Custom RSS Feed URL", "values")  # type: ignore

    if preset_name == "Custom URL":
        return str(custom_url) if custom_url else ""

    return PRESET_PODCASTS.get(str(preset_name), "")


class Podcast(Service):
    """Podcast service for monitoring and managing podcast content."""

    class new_episode(Action):
        """Triggered when a new episode is published for a podcast."""

        def __init__(self) -> None:
            super().__init__(
                "Triggered when a new episode is published on the specified podcast feed",
                _get_podcast_selection_fields(),
                "*/15 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if a new episode has been published."""
            try:
                rss_url = _resolve_rss_url(area_action.config)

                if not rss_url or not rss_url.strip():
                    logger.error("RSS Feed URL is required")
                    return False

                episodes = self.service._get_episodes_from_rss(rss_url)  # type: ignore

                if not episodes:
                    return False

                episode_guids = {ep["guid"] for ep in episodes}
                previous_guids = set(
                    area_action.last_state.get("episode_guids", [])
                    if area_action.last_state
                    else []
                )

                if (
                    not area_action.last_state
                    or "episode_guids" not in area_action.last_state
                ):
                    area_action.last_state = {"episode_guids": list(episode_guids)}
                    session.add(area_action)
                    session.commit()
                    return False

                new_guids = episode_guids - previous_guids

                area_action.last_state = {"episode_guids": list(episode_guids)}
                session.add(area_action)
                session.commit()

                return len(new_guids) > 0

            except PodcastApiError as e:
                logger.error(f"Podcast new_episode check error: {e.message}")
                return False
            except Exception as e:
                logger.error(f"Podcast new_episode unexpected error: {str(e)}")
                return False

    class episode_count_threshold(Action):
        """Triggered when the number of episodes exceeds a threshold."""

        def __init__(self) -> None:
            config_schema = _get_podcast_selection_fields() + [
                {"name": "Episode Count Threshold", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when the total number of episodes exceeds the specified threshold",
                config_schema,
                "0 0 * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if episode count exceeds threshold."""
            try:
                rss_url = _resolve_rss_url(area_action.config)
                threshold_str = get_component(
                    area_action.config, "Episode Count Threshold", "values"
                )  # type: ignore

                if not rss_url or not rss_url.strip():
                    logger.error("RSS Feed URL is required")
                    return False

                try:
                    threshold = int(threshold_str) if threshold_str else 0
                except (ValueError, TypeError):
                    logger.error(f"Invalid threshold value: {threshold_str}")
                    return False

                episodes = self.service._get_episodes_from_rss(rss_url)  # type: ignore
                current_count = len(episodes)

                previous_count = (
                    area_action.last_state.get("count", 0)
                    if area_action.last_state
                    else 0
                )

                if not area_action.last_state or "count" not in area_action.last_state:
                    area_action.last_state = {"count": current_count}
                    session.add(area_action)
                    session.commit()
                    return False

                area_action.last_state = {"count": current_count}
                session.add(area_action)
                session.commit()

                return current_count >= threshold and previous_count < threshold

            except PodcastApiError as e:
                logger.error(f"Podcast episode_count_threshold error: {e.message}")
                return False
            except Exception as e:
                logger.error(
                    f"Podcast episode_count_threshold unexpected error: {str(e)}"
                )
                return False

    class keyword_in_title(Action):
        """Triggered when a new episode title contains a specific keyword."""

        def __init__(self) -> None:
            config_schema = _get_podcast_selection_fields() + [
                {"name": "Keyword", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a new episode is published with a title containing the keyword",
                config_schema,
                "*/15 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if new episode title contains keyword."""
            try:
                rss_url = _resolve_rss_url(area_action.config)
                keyword = get_component(area_action.config, "Keyword", "values")  # type: ignore

                if not rss_url or not rss_url.strip():
                    logger.error("RSS Feed URL is required")
                    return False

                if not keyword or not keyword.strip():
                    logger.error("Keyword is required")
                    return False

                keyword_lower = keyword.lower()

                episodes = self.service._get_episodes_from_rss(rss_url)  # type: ignore

                if not episodes:
                    return False

                matching_episode_guids = {
                    ep["guid"]
                    for ep in episodes
                    if keyword_lower in ep["title"].lower()
                }

                previous_matching_guids = set(
                    area_action.last_state.get("matching_guids", [])
                    if area_action.last_state
                    else []
                )

                if (
                    not area_action.last_state
                    or "matching_guids" not in area_action.last_state
                ):
                    area_action.last_state = {
                        "matching_guids": list(matching_episode_guids)
                    }
                    session.add(area_action)
                    session.commit()
                    return False

                new_matching = matching_episode_guids - previous_matching_guids

                area_action.last_state = {
                    "matching_guids": list(matching_episode_guids)
                }
                session.add(area_action)
                session.commit()

                return len(new_matching) > 0

            except PodcastApiError as e:
                logger.error(f"Podcast keyword_in_title error: {e.message}")
                return False
            except Exception as e:
                logger.error(f"Podcast keyword_in_title unexpected error: {str(e)}")
                return False

    class log_podcast_info(Reaction):
        """Log information about a podcast feed."""

        def __init__(self) -> None:
            config_schema = _get_podcast_selection_fields() + [
                {"name": "Log Message", "type": "textarea", "values": []},
            ]
            super().__init__(
                "Log custom message with podcast information", config_schema
            )

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            """Log podcast information."""
            try:
                rss_url = _resolve_rss_url(area_action.config)
                log_message = get_component(area_action.config, "Log Message", "values")  # type: ignore

                if not rss_url or not rss_url.strip():
                    logger.error("RSS Feed URL is required")
                    return

                podcast_info = self.service._get_podcast_info(rss_url)  # type: ignore

                message = log_message if log_message else "Podcast update"
                logger.info(
                    f"{message} - Podcast: {podcast_info.get('title', 'Unknown')}, "
                    f"Episodes: {podcast_info.get('episode_count', 0)}"
                )

            except PodcastApiError as e:
                logger.error(f"Podcast log_podcast_info error: {e.message}")
            except Exception as e:
                logger.error(f"Podcast log_podcast_info unexpected error: {str(e)}")

    class save_episode_list(Reaction):
        """Save the list of latest episodes to a text format."""

        def __init__(self) -> None:
            config_schema = _get_podcast_selection_fields() + [
                {
                    "name": "Number of Episodes",
                    "type": "select",
                    "values": ["5", "10", "20", "50"],
                },
            ]
            super().__init__(
                "Log the list of latest episodes from the podcast feed", config_schema
            )

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            """Save episode list."""
            try:
                rss_url = _resolve_rss_url(area_action.config)
                num_episodes_str = get_component(
                    area_action.config, "Number of Episodes", "values"
                )  # type: ignore

                if not rss_url or not rss_url.strip():
                    logger.error("RSS Feed URL is required")
                    return

                try:
                    num_episodes = int(num_episodes_str) if num_episodes_str else 10
                except (ValueError, TypeError):
                    num_episodes = 10

                episodes = self.service._get_episodes_from_rss(rss_url)  # type: ignore
                episodes = episodes[:num_episodes]

                episode_list = "\n".join(
                    [
                        f"{i + 1}. {ep['title']} ({ep['published']})"
                        for i, ep in enumerate(episodes)
                    ]
                )

                logger.info(f"Latest {num_episodes} episodes:\n{episode_list}")

            except PodcastApiError as e:
                logger.error(f"Podcast save_episode_list error: {e.message}")
            except Exception as e:
                logger.error(f"Podcast save_episode_list unexpected error: {str(e)}")

    def __init__(self) -> None:
        super().__init__(
            description="Monitor and manage podcast RSS feeds",
            category=ServiceCategory.MEDIA,
            color="#9b59b6",
            img_url="/images/Podcast_logo.webp",
            oauth=False,
        )

    def _get_episodes_from_rss(self, rss_url: str) -> List[Dict[str, Any]]:
        """Parse RSS feed and extract episodes."""
        try:
            response = requests.get(rss_url, timeout=10)

            if response.status_code != 200:
                raise PodcastApiError(
                    f"Failed to fetch RSS feed: {response.status_code}"
                )

            root = ET.fromstring(response.content)

            channel = root.find("channel")
            if channel is None:
                raise PodcastApiError("Invalid RSS feed format: no channel found")

            episodes = []
            for item in channel.findall("item"):
                title_elem = item.find("title")
                guid_elem = item.find("guid")
                pub_date_elem = item.find("pubDate")
                description_elem = item.find("description")
                link_elem = item.find("link")

                episode = {
                    "title": title_elem.text if title_elem is not None else "Untitled",
                    "guid": guid_elem.text if guid_elem is not None else "",
                    "published": pub_date_elem.text
                    if pub_date_elem is not None
                    else "",
                    "description": description_elem.text
                    if description_elem is not None
                    else "",
                    "link": link_elem.text if link_elem is not None else "",
                }

                episodes.append(episode)

            return episodes

        except requests.RequestException as e:
            raise PodcastApiError(f"Network error: {str(e)}")
        except ET.ParseError as e:
            raise PodcastApiError(f"XML parsing error: {str(e)}")
        except Exception as e:
            raise PodcastApiError(f"Unexpected error: {str(e)}")

    def _get_podcast_info(self, rss_url: str) -> Dict[str, Any]:
        """Get podcast metadata from RSS feed."""
        try:
            response = requests.get(rss_url, timeout=10)

            if response.status_code != 200:
                raise PodcastApiError(
                    f"Failed to fetch RSS feed: {response.status_code}"
                )

            root = ET.fromstring(response.content)
            channel = root.find("channel")

            if channel is None:
                raise PodcastApiError("Invalid RSS feed format")

            title_elem = channel.find("title")
            description_elem = channel.find("description")
            link_elem = channel.find("link")

            episode_count = len(channel.findall("item"))

            return {
                "title": title_elem.text if title_elem is not None else "Unknown",
                "description": description_elem.text
                if description_elem is not None
                else "",
                "link": link_elem.text if link_elem is not None else "",
                "episode_count": episode_count,
            }

        except requests.RequestException as e:
            raise PodcastApiError(f"Network error: {str(e)}")
        except ET.ParseError as e:
            raise PodcastApiError(f"XML parsing error: {str(e)}")
        except Exception as e:
            raise PodcastApiError(f"Unexpected error: {str(e)}")
