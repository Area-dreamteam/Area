from crontab import CronTab
from pathlib import Path


def newJob(action_id: int):
    cron = CronTab(user="root")

    job = cron.new(
        command=f"python {Path(__file__).resolve().parent}/cron_scripts/time.py {action_id}"
    )
    # job.setall("*/1 * * * *")
    job.minutes.every(1)

    cron.write()

    for job in cron:
        print(job)
