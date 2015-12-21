from suma.core.models import Link, ClickCounter, Stat


def test_add_click(db_session, stat_svc):
    link = Link(url='http://google.com/test', hashid='1234')
    db_session.add(link)
    db_session.flush()
    stat_svc.add_click(link.id)
    assert db_session.query(Stat).count() == 1
    assert db_session.query(ClickCounter).count() == 1
    assert db_session.query(ClickCounter).get(link.id).counter == 1
    stat_svc.add_click(link.id)
    assert db_session.query(ClickCounter).count() == 1
    assert db_session.query(ClickCounter).get(link.id).counter == 2
