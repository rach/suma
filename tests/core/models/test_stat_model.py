from suma.core.models import Link, Stat, ClickCounter
from hashlib import sha1
from sqlalchemy.exc import IntegrityError
import pytest


@pytest.fixture
def link():
    return Link(
        hashid='12345',
        url='http://google.com/test'
    )


def test_create_stat(db_session, link):
    stat = Stat(
        link=link
    )
    db_session.add(stat)
    assert db_session.query(Stat).count() == 1


def test_stat_link_not_null_constraint(db_session):
    stat = Stat(
    )
    db_session.add(stat)
    with pytest.raises(IntegrityError) as excinfo:
        db_session.flush()
    assert 'violates not-null constraint' in str(excinfo.value)


def test_create_click(db_session, link):
    click = ClickCounter(
        link=link
    )
    db_session.add(click)
    db_session.flush()
    assert click.counter == 1
    assert db_session.query(ClickCounter).count() == 1


def test_click_link_not_null_constrain(db_session):
    click = ClickCounter(
    )
    db_session.add(click)
    with pytest.raises(IntegrityError) as excinfo:
        db_session.flush()
    assert 'violates not-null constraint' in str(excinfo.value)
