from crontab import CronTab
from core.config import settings
from models.services.action import Action
from models.areas.area import Area
from cron.cron import newJob
from models.areas import AreaAction
from core.logger import logger
from sqlmodel import select
from sqlmodel import Session
from typing import List
from core.engine import engine


def startupCron():
    cron = CronTab(user=settings.CRON_USER)
    if cron.lines != 0:
        cron.remove_all()

    with Session(engine) as session:
        actions: List[AreaAction] = session.exec(
            select(AreaAction)
            .join(Action, Action.id == AreaAction.action_id)
            .join(Area, Area.id == AreaAction.area_id)
            .where(
                Area.enable == True,
                Area.is_public == False,
            )
        ).all()
        for i in actions:
            newJob(i.action_id)

    logger.debug(f"Cron startup: {actions}")
