from typing import List
from crontab import CronTab
from sqlmodel import select, join
from pathlib import Path
from core.engine import engine
from sqlmodel import Session

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
    job.setall(actions_config.interval)

    cron.write()

    for job in cron:
        print(job)
