from suma.celery import task 
from goose import Goose
import requests
import uuid


@task()
def get_link_data_task(link_id):
    dbsession = get_link_data_task.dbsession
    services = get_link_data_task.services
    flags = get_link_data_task.flags
    if not flags:
        return
    link = services.link.get_link_by_id(link_id)
    if link is None:
        return
    html = None
    if 'screenshot' in flags:
        data, html = services.screenshot.capture(link.url, 1024, 800)
        # TODO: Investigate if this way of generating filename can create clashes
        # TODO: Delete the previous file if it exist
        filename = services.file.create(data,  str(uuid.uuid4()) + '.png', 'screenshots')
        link.meta['screenshot'] = filename

    if 'html' in flags:
        link.meta['html'] = html if html else requests.get(link.url).text

    # this should move to a service too
    if 'text' in flags or 'title' in flags:
        goose = Goose()
        a = goose.extract(raw_html=html if html else requests.get(link.url).text)
        if 'text' in flags:
            link.meta['text'] = a.cleaned_text

        if 'title' in flags:
            link.meta['title'] = a.title
    dbsession.commit() #  we are outside the web transaction


@task()
def add_click_task(link_id, ip, referer):
    dbsession = add_click_task.dbsession
    services = add_click_task.services
    services.stat.add_click(link_id, referer, ip)
    dbsession.commit()
