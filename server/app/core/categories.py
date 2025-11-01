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

    @classmethod
    def get_all_values(cls) -> list[str]:
        """Get all category values as a list."""
        return [category.value for category in cls]

    @classmethod
    def get_display_name(cls, category: str) -> str:
        """Get a human-readable display name for a category."""
        display_names = {
            cls.COMMUNICATION: "Communication",
            cls.SOCIAL: "Social Media",
            cls.MEDIA: "Media",
            cls.MUSIC: "Music",
            cls.MOVIE: "Movies & TV",
            cls.GAMING: "Gaming",
            cls.LIFESTYLE: "Lifestyle",
            cls.CALENDAR: "Calendar",
            cls.MAIL: "Email",
            cls.PRODUCTIVITY: "Productivity",
            cls.DEVELOPER: "Developer Tools",
            cls.FITNESS: "Fitness",
            cls.TIME: "Time & Date",
            cls.WEATHER: "Weather",
        }
        return display_names.get(category, category.capitalize())

    @classmethod
    def validate(cls, category: str) -> bool:
        """Check if a category value is valid.

        Args:
            category: The category value to validate

        Returns:
            True if the category is valid, False otherwise
        """
        try:
            cls(category)
            return True
        except ValueError:
            return False
