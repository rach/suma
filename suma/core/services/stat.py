from types import IntType, LongType
from suma.core.services.interfaces import IStatService
from zope.interface import implementer
from suma.core.models import Stat, ClickCounter
from structlog import get_logger
from sqlalchemy.exc import IntegrityError
log = get_logger()


@implementer(IStatService)
class StatService(object):

    def __init__(self, dbsession):
        self.dbsession = dbsession

    def add_click(self, link_id, ip=None, referer=None):
        """
        The code may look more complex than it should but it was made to handle
        the edge case of concurrent transaction. Counter doesn't exist yet when
        we fetch but it exist when we try to write it to the DB.
        """
        assert type(link_id) in [IntType, LongType], "link_id is not an integer: %r" % link_id

        lcounter = self.get_counter_by_link_id(link_id)
        if lcounter:
            lcounter.counter = lcounter.counter + 1
            self.dbsession.add(lcounter)
        if not lcounter:
            lcounter = ClickCounter(
                id=link_id,
                counter=1
            )
            self.dbsession.begin_nested()
            try:
                self.dbsession.add(lcounter)
                self.dbsession.commit()
            except IntegrityError:
                self.dbsession.rollback()
                lcounter = self.get_counter_by_link_id(link_id)
                lcounter.counter = lcounter.counter + 1
                self.dbsession.add(lcounter)

        stat = Stat(
            link_id=link_id,
            ip=ip,
            referer=referer
        )
        self.dbsession.add(stat)
        return lcounter, stat

    def get_counter_by_link_id(self, link_id):
        return self.dbsession.query(ClickCounter).get(link_id)
