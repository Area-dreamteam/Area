"""Service category definitions."""

from enum import Enum


class ServiceCategory(str, Enum):
    """Service category enumeration."""

    COMMUNICATION = "communication"
    SOCIAL = "social"

    MEDIA = "media"
    MUSIC = "music"
    MOVIE = "movie"
    GAMING = "gaming"
    STREAMING = "gaming"

    LIFESTYLE = "lifestyle"
    CALENDAR = "calendar"
    MAIL = "mail"

    PRODUCTIVITY = "productivity"

    DEVELOPER = "developer"

    FITNESS = "fitness"

    TIME = "time"
    WEATHER = "weather"
