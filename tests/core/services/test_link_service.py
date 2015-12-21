from suma.core.models import Link


def test_create_link(db_session, link_svc):
    link_svc.create_link('http://google.com/test')
    assert db_session.query(Link).filter(Link.url == 'http://google.com/test').count() == 1


def test_create_link_with_user_id(db_session, link_svc):
    link_svc.create_link('http://google.com/test', 1)
    assert (
        db_session.query(Link).
        filter(Link.url == 'http://google.com/test', Link.user_id == 1).count() == 1
    )


def test_create_duplicate_link(db_session, link_svc):
    l1, created = link_svc.create_link('http://google.com/test')
    assert created is True
    l2, created = link_svc.create_link('http://google.com/test')
    assert created is False
    assert l1 == l2
    assert db_session.query(Link).filter(Link.url == 'http://google.com/test').count() == 1


def test_get_link_by_id_or_hashid(db_session, link_svc):
    l1 = Link(hashid='1234', url='http://google.com/test')
    db_session.add(l1)
    db_session.flush()
    l2 = link_svc.get_link_by_id_or_hashid(l1.id)
    assert l2 is not None
    assert l1 == l2
    l3 = link_svc.get_link_by_id_or_hashid('1234')
    assert l3 is not None
    assert l1 == l3


def test_get_link_by_id(db_session, link_svc):
    l1 = Link(hashid='1234', url='http://google.com/test')
    db_session.add(l1)
    db_session.flush()
    l2 = link_svc.get_link_by_id(l1.id)
    assert l2 is not None
    assert l1 == l2


def test_get_link_by_url(db_session, link_svc):
    l1 = Link(hashid='1234', url='http://google.com/test')
    db_session.add(l1)
    db_session.flush()
    l2 = link_svc.get_link_by_url('http://google.com/test')
    assert l2 is not None
    assert l1 == l2


def test_get_link_by_url_with_user_id(db_session, link_svc):
    l1 = Link(hashid='1234', user_id=1, url='http://google.com/test')
    db_session.add(l1)
    db_session.flush()
    l2 = link_svc.get_link_by_url('http://google.com/test')
    assert l2 is None
    l3 = link_svc.get_link_by_url('http://google.com/test', user_id=1)
    assert l3 is not None
    assert l1 == l3


def test_get_link_by_hashid(db_session, link_svc):
    l1 = Link(hashid='1234', url='http://google.com/test')
    db_session.add(l1)
    db_session.flush()
    l2 = link_svc.get_link_by_hashid('1234')
    assert l2 is not None
    assert l1 == l2


def test_get_link_by_unknown_hashid(db_session, link_svc):
    l1 = Link(hashid='1234', url='http://google.com/test')
    db_session.add(l1)
    db_session.flush()
    l2 = link_svc.get_link_by_hashid('5678')
    assert l2 is None


def test_get_link_by_id_or_hashid_with_unknown_hashid(db_session, link_svc):
    l1 = Link(hashid='1234', url='http://google.com/test')
    db_session.add(l1)
    db_session.flush()
    l2 = link_svc.get_link_by_id_or_hashid('abcd')
    assert l2 is None


def test_get_link_by_id_or_hashid_with_unknown_hashid(db_session, link_svc):
    l1 = Link(hashid='1234', url='http://google.com/test')
    db_session.add(l1)
    db_session.flush()
    l2 = link_svc.get_link_by_id_or_hashid(-1)
    assert l2 is None


def test_ban_url(db_session, link_svc):
    l1 = Link(hashid='aaaa', url='http://google.com/test')
    l2 = Link(hashid='bbbb', url='http://google.com/random')
    l3 = Link(hashid='cccc', url='http://google.com/test?v=1')
    db_session.add(l1)
    db_session.add(l2)
    db_session.add(l3)
    db_session.flush()
    link_svc.ban_url('http://google.com/test', mode='url')
    assert l1.is_banned
    assert not l2.is_banned
    assert not l3.is_banned


def test_ban_url_path(db_session, link_svc):
    l1 = Link(hashid='aaaa', url='http://google.com/test')
    l2 = Link(hashid='bbbb', url='http://google.com/random')
    l3 = Link(hashid='cccc', url='http://google.com/test?v=1')
    db_session.add(l1)
    db_session.add(l2)
    db_session.add(l3)
    db_session.flush()
    link_svc.ban_url('http://google.com/test', mode='path')
    assert l1.is_banned and l3.is_banned and not l2.is_banned


def test_ban_url_netloc(db_session, link_svc):
    l1 = Link(hashid='aaaa', url='http://google.com/test')
    l2 = Link(hashid='bbbb', url='http://google.com/random')
    l3 = Link(hashid='cccc', url='http://google.com/test?v=1')
    db_session.add(l1)
    db_session.add(l2)
    db_session.add(l3)
    db_session.flush()
    link_svc.ban_url('http://google.com/test', mode='netloc')
    assert l1.is_banned and l2.is_banned and l3.is_banned
