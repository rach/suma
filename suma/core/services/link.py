from suma.core.services.interfaces import ILinkService
from zope.interface import implementer
from suma.core.models import Link, BlockingType, BlockedLink
from suma.core.models.link import create_url_hashes
from structlog import get_logger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_
from sqlalchemy.schema import Sequence
from sqlalchemy.exc import IntegrityError

log = get_logger()


@implementer(ILinkService)
class LinkService(object):

    def __init__(self, dbsession, hashid):
        self.dbsession = dbsession
        self.hashid = hashid

    def create_link(self, url, user_id=None):
        created = False
        link = self.get_link_by_url(url, user_id)
        if link:
            return link, created

        nextid = self.dbsession.execute(Sequence("link_id_seq"))
        hashid = self.hashid.encode(nextid)
        link = Link(
            id=nextid,
            user_id=user_id,
            url=url,
            hashid=hashid
        )
        self.dbsession.begin_nested()
        try:
            self.dbsession.add(link)
            self.dbsession.commit()
            created = True
        except IntegrityError:
            self.dbsession.rollback()
            link = self.get_link_by_url(url, user_id)

        return link, created

    def get_link_by_id_or_hashid(self, id_or_hashid):
        args = []
        if str(id_or_hashid).isdigit():
            args.append(Link.id == id_or_hashid)
        args.append(Link.hashid == str(id_or_hashid))
        try:
            return self.dbsession.query(Link).filter(
                or_(*args)
            ).one()
        except NoResultFound:
            return None

    def get_link_by_url(self, url, user_id=None):
        l_query = self.dbsession.query(Link)
        return l_query.filter(Link.url == url, Link.user_id == user_id).first()

    def get_link_by_id(self, id):
        return self.dbsession.query(Link).filter(Link.id == id).first()

    def get_link_by_hashid(self, hashid):
        return self.dbsession.query(Link).filter(Link.hashid == hashid).first()

    def ban_url(self, url, mode='url'):
        assert mode in ('url', 'netloc', 'path'),\
            'Bad mode is not "url", "netloc" or "path"'
        hash_url, hash_netloc, hash_path = create_url_hashes(url)
        hdict = dict(zip(('url', 'netloc', 'path'), (hash_url, hash_netloc, hash_path)))
        btype = BlockingType.from_string(mode)
        bl = BlockedLink(
            hash=hdict[mode],
            url=url,
            type=btype
        )
        self.dbsession.begin_nested()
        try:
            self.dbsession.add(bl)
            self.dbsession.commit()
        except IntegrityError:
            # already blocked so we me ignore
            self.dbsession.rollback()
