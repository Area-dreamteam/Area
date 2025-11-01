"""Date and Time automation service.

Provides time-based triggers for automation workflows.
No OAuth required - purely time-based condition checking.
"""

from models import AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, get_component
from core.categories import ServiceCategory
from datetime import datetime, time as dt_time
from core.logger import logger


class DateAndTimeError(Exception):
    """Date and Time service-specific errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DateAndTime(Service):
    """Date and Time automation service for time-based triggers."""

    class every_minute(Action):
        """Triggered every minute."""

        service: "DateAndTime"

        def __init__(self) -> None:
            super().__init__("Triggered every minute", [], "* * * * *")

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Always returns True - triggers every minute."""
            try:
                return True
            except Exception as e:
                logger.error(f"DateAndTime every_minute error: {str(e)}")
                return False

    class every_hour_at(Action):
        """Triggered once per hour at a specific minute (00, 15, 30, or 45)."""

        service: "DateAndTime"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Minute",
                    "type": "select",
                    "values": ["00", "15", "30", "45"],
                },
            ]
            super().__init__(
                "Triggered once per hour at :00, :15, :30 or :45 minutes",
                config_schema,
                "* * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if current minute matches selected interval."""
            try:
                current_time = datetime.now()
                selected_minute_str = get_component(
                    area_action.config, "Minute", "values"
                )

                if not selected_minute_str:
                    logger.error("No minute value configured")
                    return False

                selected_minute = int(selected_minute_str)

                if selected_minute == current_time.minute:
                    current_hour_key = f"{current_time.year}-{current_time.month}-{current_time.day}-{current_time.hour}"
                    last_trigger = (
                        area_action.last_state.get("last_trigger_hour")
                        if area_action.last_state
                        else None
                    )

                    if last_trigger != current_hour_key:
                        area_action.last_state = {"last_trigger_hour": current_hour_key}
                        session.add(area_action)
                        session.commit()
                        return True

                return False
            except (ValueError, TypeError) as e:
                logger.error(f"DateAndTime every_hour_at error: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"DateAndTime every_hour_at unexpected error: {str(e)}")
                return False

    class specific_time_daily(Action):
        """Triggered daily at a specific time (HH:MM format)."""

        service: "DateAndTime"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Hour",
                    "type": "select",
                    "values": [f"{h:02d}" for h in range(24)],
                },
                {
                    "name": "Minute",
                    "type": "select",
                    "values": [f"{m:02d}" for m in range(0, 60, 5)],
                },
            ]
            super().__init__(
                "Triggered daily at a specific time (HH:MM)", config_schema, "* * * * *"
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if current time matches configured time."""
            try:
                current_time = datetime.now()
                hour_str = get_component(area_action.config, "Hour", "values")
                minute_str = get_component(area_action.config, "Minute", "values")

                if not hour_str or not minute_str:
                    logger.error("Hour or Minute not configured")
                    return False

                target_hour = int(hour_str)
                target_minute = int(minute_str)

                if (
                    current_time.hour == target_hour
                    and current_time.minute == target_minute
                ):
                    current_day_key = (
                        f"{current_time.year}-{current_time.month}-{current_time.day}"
                    )
                    last_trigger = (
                        area_action.last_state.get("last_trigger_day")
                        if area_action.last_state
                        else None
                    )

                    if last_trigger != current_day_key:
                        area_action.last_state = {"last_trigger_day": current_day_key}
                        session.add(area_action)
                        session.commit()
                        return True

                return False
            except (ValueError, TypeError) as e:
                logger.error(f"DateAndTime specific_time_daily error: {str(e)}")
                return False
            except Exception as e:
                logger.error(
                    f"DateAndTime specific_time_daily unexpected error: {str(e)}"
                )
                return False

    class specific_day_of_week(Action):
        """Triggered on specific day(s) of the week at a specific time."""

        service: "DateAndTime"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Days",
                    "type": "check_list",
                    "values": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday",
                    ],
                },
                {
                    "name": "Hour",
                    "type": "select",
                    "values": [f"{h:02d}" for h in range(24)],
                },
                {
                    "name": "Minute",
                    "type": "select",
                    "values": [f"{m:02d}" for m in range(0, 60, 5)],
                },
            ]
            super().__init__(
                "Triggered on specific day(s) of the week at a specific time",
                config_schema,
                "* * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if current day and time match configuration."""
            try:
                current_time = datetime.now()
                selected_days = get_component(area_action.config, "Days", "values")
                hour_str = get_component(area_action.config, "Hour", "values")
                minute_str = get_component(area_action.config, "Minute", "values")

                if not selected_days or not hour_str or not minute_str:
                    logger.error("Days, Hour or Minute not configured")
                    return False

                target_hour = int(hour_str)
                target_minute = int(minute_str)

                day_mapping = {
                    "Monday": 0,
                    "Tuesday": 1,
                    "Wednesday": 2,
                    "Thursday": 3,
                    "Friday": 4,
                    "Saturday": 5,
                    "Sunday": 6,
                }

                current_day = current_time.weekday()

                if isinstance(selected_days, list):
                    day_numbers = [
                        day_mapping.get(day)
                        for day in selected_days
                        if day in day_mapping
                    ]
                else:
                    day_numbers = (
                        [day_mapping.get(selected_days)]
                        if selected_days in day_mapping
                        else []
                    )

                if current_day not in day_numbers:
                    return False

                if (
                    current_time.hour == target_hour
                    and current_time.minute == target_minute
                ):
                    current_day_key = (
                        f"{current_time.year}-{current_time.month}-{current_time.day}"
                    )
                    last_trigger = (
                        area_action.last_state.get("last_trigger_day")
                        if area_action.last_state
                        else None
                    )

                    if last_trigger != current_day_key:
                        area_action.last_state = {"last_trigger_day": current_day_key}
                        session.add(area_action)
                        session.commit()
                        return True

                return False
            except (ValueError, TypeError) as e:
                logger.error(f"DateAndTime specific_day_of_week error: {str(e)}")
                return False
            except Exception as e:
                logger.error(
                    f"DateAndTime specific_day_of_week unexpected error: {str(e)}"
                )
                return False

    class every_n_minutes(Action):
        """Triggered every N minutes (5, 10, 15, 30)."""

        service: "DateAndTime"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Interval (minutes)",
                    "type": "select",
                    "values": ["5", "10", "15", "30"],
                },
            ]
            super().__init__(
                "Triggered every N minutes (5, 10, 15, or 30)",
                config_schema,
                "* * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if current time is a multiple of the interval."""
            try:
                current_time = datetime.now()
                interval_str = get_component(
                    area_action.config, "Interval (minutes)", "values"
                )

                if not interval_str:
                    logger.error("Interval not configured")
                    return False

                interval = int(interval_str)

                if current_time.minute % interval == 0:
                    current_minute_key = f"{current_time.year}-{current_time.month}-{current_time.day}-{current_time.hour}-{current_time.minute}"
                    last_trigger = (
                        area_action.last_state.get("last_trigger_minute")
                        if area_action.last_state
                        else None
                    )

                    if last_trigger != current_minute_key:
                        area_action.last_state = {
                            "last_trigger_minute": current_minute_key
                        }
                        session.add(area_action)
                        session.commit()
                        return True

                return False
            except (ValueError, TypeError) as e:
                logger.error(f"DateAndTime every_n_minutes error: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"DateAndTime every_n_minutes unexpected error: {str(e)}")
                return False

    class specific_date(Action):
        """Triggered on a specific date at a specific time."""

        service: "DateAndTime"

        def __init__(self) -> None:
            config_schema = [
                {"name": "Year", "type": "input", "values": []},
                {
                    "name": "Month",
                    "type": "select",
                    "values": [f"{m:02d}" for m in range(1, 13)],
                },
                {
                    "name": "Day",
                    "type": "select",
                    "values": [f"{d:02d}" for d in range(1, 32)],
                },
                {
                    "name": "Hour",
                    "type": "select",
                    "values": [f"{h:02d}" for h in range(24)],
                },
                {
                    "name": "Minute",
                    "type": "select",
                    "values": [f"{m:02d}" for m in range(0, 60, 5)],
                },
            ]
            super().__init__(
                "Triggered on a specific date at a specific time (one-time trigger)",
                config_schema,
                "* * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if current date and time match configuration."""
            try:
                current_time = datetime.now()

                already_triggered = (
                    area_action.last_state.get("triggered", False)
                    if area_action.last_state
                    else False
                )

                if already_triggered:
                    return False

                year_str = get_component(area_action.config, "Year", "values")
                month_str = get_component(area_action.config, "Month", "values")
                day_str = get_component(area_action.config, "Day", "values")
                hour_str = get_component(area_action.config, "Hour", "values")
                minute_str = get_component(area_action.config, "Minute", "values")

                if not all([year_str, month_str, day_str, hour_str, minute_str]):
                    logger.error("Date/Time not fully configured")
                    return False

                target_year = int(year_str)
                target_month = int(month_str)
                target_day = int(day_str)
                target_hour = int(hour_str)
                target_minute = int(minute_str)

                if (
                    current_time.year == target_year
                    and current_time.month == target_month
                    and current_time.day == target_day
                    and current_time.hour == target_hour
                    and current_time.minute == target_minute
                ):
                    area_action.last_state = {"triggered": True}
                    session.add(area_action)
                    session.commit()
                    return True

                return False
            except (ValueError, TypeError) as e:
                logger.error(f"DateAndTime specific_date error: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"DateAndTime specific_date unexpected error: {str(e)}")
                return False

    class time_range(Action):
        """Triggered when current time is within a specified range."""

        service: "DateAndTime"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Start Hour",
                    "type": "select",
                    "values": [f"{h:02d}" for h in range(24)],
                },
                {
                    "name": "Start Minute",
                    "type": "select",
                    "values": [f"{m:02d}" for m in range(0, 60, 5)],
                },
                {
                    "name": "End Hour",
                    "type": "select",
                    "values": [f"{h:02d}" for h in range(24)],
                },
                {
                    "name": "End Minute",
                    "type": "select",
                    "values": [f"{m:02d}" for m in range(0, 60, 5)],
                },
            ]
            super().__init__(
                "Triggered continuously when current time is within specified range (triggers once per entry)",
                config_schema,
                "* * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if current time is within the specified range."""
            try:
                current_time = datetime.now()

                start_hour_str = get_component(
                    area_action.config, "Start Hour", "values"
                )
                start_minute_str = get_component(
                    area_action.config, "Start Minute", "values"
                )
                end_hour_str = get_component(area_action.config, "End Hour", "values")
                end_minute_str = get_component(
                    area_action.config, "End Minute", "values"
                )

                if not all(
                    [start_hour_str, start_minute_str, end_hour_str, end_minute_str]
                ):
                    logger.error("Time range not fully configured")
                    return False

                start_hour = int(start_hour_str)
                start_minute = int(start_minute_str)
                end_hour = int(end_hour_str)
                end_minute = int(end_minute_str)

                current_time_only = dt_time(current_time.hour, current_time.minute)
                start_time = dt_time(start_hour, start_minute)
                end_time = dt_time(end_hour, end_minute)

                if start_time <= end_time:
                    in_range = start_time <= current_time_only <= end_time
                else:
                    in_range = (
                        current_time_only >= start_time or current_time_only <= end_time
                    )

                was_in_range = (
                    area_action.last_state.get("in_range", False)
                    if area_action.last_state
                    else False
                )

                area_action.last_state = {"in_range": in_range}
                session.add(area_action)
                session.commit()

                return in_range and not was_in_range

            except (ValueError, TypeError) as e:
                logger.error(f"DateAndTime time_range error: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"DateAndTime time_range unexpected error: {str(e)}")
                return False

    class business_hours(Action):
        """Triggered during business hours (Monday-Friday, configurable time range)."""

        service: "DateAndTime"

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Start Hour",
                    "type": "select",
                    "values": [f"{h:02d}" for h in range(24)],
                },
                {
                    "name": "End Hour",
                    "type": "select",
                    "values": [f"{h:02d}" for h in range(24)],
                },
            ]
            super().__init__(
                "Triggered when entering business hours (Monday-Friday, specified hours, triggers once per entry)",
                config_schema,
                "* * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            """Check if currently in business hours."""
            try:
                current_time = datetime.now()

                if current_time.weekday() > 4:
                    area_action.last_state = {"in_business_hours": False}
                    session.add(area_action)
                    session.commit()
                    return False

                start_hour_str = get_component(
                    area_action.config, "Start Hour", "values"
                )
                end_hour_str = get_component(area_action.config, "End Hour", "values")

                if not start_hour_str or not end_hour_str:
                    logger.error("Business hours not configured")
                    return False

                start_hour = int(start_hour_str)
                end_hour = int(end_hour_str)

                in_business_hours = start_hour <= current_time.hour < end_hour

                was_in_business_hours = (
                    area_action.last_state.get("in_business_hours", False)
                    if area_action.last_state
                    else False
                )

                area_action.last_state = {"in_business_hours": in_business_hours}
                session.add(area_action)
                session.commit()

                return in_business_hours and not was_in_business_hours

            except (ValueError, TypeError) as e:
                logger.error(f"DateAndTime business_hours error: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"DateAndTime business_hours unexpected error: {str(e)}")
                return False

    def __init__(self) -> None:
        super().__init__(
            "Date and Time triggers for automation workflows",
            ServiceCategory.TIME,
            "#4a4d4b",
            "/images/DateAndTime_logo.webp",
            False,
        )

    def is_connected(self, session: Session, user_id: int) -> bool:
        """Date and Time service is always available (no connection required)."""
        return True
