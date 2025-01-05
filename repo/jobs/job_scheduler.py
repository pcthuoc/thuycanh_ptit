import logging
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from jobs.task import check_hengio_tasks
from jobs.task import check_and_control_system, control_pump_job

# Thiết lập logger
logger = logging.getLogger(__name__)

def create_scheduler():
    """
    Tạo scheduler với cấu hình phù hợp.
    """
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor()
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 3,
        'misfire_grace_time': 60
    }
    scheduler = BlockingScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone="Asia/Ho_Chi_Minh"
    )
    return scheduler


def config_job(scheduler):
    """
    Cấu hình các công việc cho scheduler.
    """
    #scheduler.add_job(check_hengio_tasks, 'interval', seconds=5, id='check_hengio_tasks', replace_existing=True)
    #scheduler.add_job(check_and_control_system, 'interval', seconds=15, id='check_and_control_system', replace_existing=True)
    scheduler.add_job(control_pump_job, 'interval', seconds=5, id='control_pump_job', replace_existing=True)
    return scheduler


def start_scheduler():
    """
    Bắt đầu scheduler và xử lý lỗi nếu có.
    """
    while True:
        try:
            print("Tạo scheduler...")
            scheduler = create_scheduler()
            print("Cấu hình job...")
            config_job(scheduler)
            print("Bắt đầu scheduler...")
            scheduler.start()
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")
            print("Restarting scheduler...")
