from typing import List
from crontab import CronTab
from sqlmodel import select, join
from pathlib import Path
from core.engine import engine
from sqlmodel import Session
from core.logger import logger

from models.services.action import Action


def newJob(action_id: int):
    cron = CronTab(user="root")

    job = cron.new(
        command=f"python {Path(__file__).resolve().parent}/cron_scripts/time.py {action_id}"
    )
    with Session(engine) as session:
        actions_config: Action = session.exec(
            select(Action).where(
                Action.id == action_id,
            )
        ).first()
        if not actions_config:
            logger.error(f"Cron Error: action_id not found {action_id}")
            return
    job.setall(actions_config.interval)

    cron.write()
    logger.debug(f"Cron: new cron for action {action_id}")

    for job in cron:
        print(job)

def deleteJob(action_id: int):
    cron = CronTab(user="root")

    jobs_to_remove = [job for job in cron if str(action_id) in job.command]

    if not jobs_to_remove:
        logger.error(f"Cron Error: action_id not found {action_id}")
        return
    for job in jobs_to_remove:
        logger.debug(f"Cron: deleted action, {action_id}")
        cron.remove(job)
    cron.write()

def isCronExists(action_id: int):
    cron = CronTab(user="root")
    
    existing_jobs: list = [job for job in cron if str(action_id) in job.command]
    if len(existing_jobs) == 0:
        return False
    return True
