from app.models import Task
from app.celery_app import celery
from app.config import IPDATA_URL, IPDATA_TOKEN
import requests
from app.models import db, LocationInfo


@celery.task(max_retries=3)
def process_task(task_ip: str, task_id: int) -> dict:
    """
       A celery task function that processes a given task IP and task ID, and returns a dictionary.
    """

    sess = requests.Session()
    sess.headers.update({"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"})

    try:
        resp = sess.get(url=f'{IPDATA_URL}{task_ip}?api-key={IPDATA_TOKEN}')
    except requests.exceptions.ConnectionError:
        return {'status': False, 'error': 'ConnectionError'}

    if "reserved IP address" in resp.text:
        return {'status': False, 'error': 'reserved IP address'}

    try:
        with db:
            location_info = LocationInfo.parse_raw(resp.text)

            task = Task.get(Task.id == task_id)

            task.completed = True
            for field, value in location_info.model_dump().items():
                setattr(task, field, value)
            task.save()

    except Exception as e:
        print(e)
        return {'status': False, 'error': 'ParseError'}
    result = {'status': True, 'data': location_info.model_dump()}
    return {"external_api_response": result}
