from crontab import CronTab
from cron.cron import newJob
from models.areas import AreaAction
from core.logger import logger
from sqlmodel import select
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends
from core.engine import engine


def startupCron():
    cron = CronTab(user="root")
    if cron.lines != 0:
        cron.remove_all()

    with Session(engine) as session:
        actions = session.exec(select(AreaAction)).all()
        # for i in actions:
        #    newJob(
        #        "root",
        #    )

    logger.info(f"Cron startup: {actions}")
