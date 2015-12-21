from suma.core.models import Link
from hashlib import sha1
from sqlalchemy.exc import IntegrityError
import pytest


def test_create_link(db_session):
    link = Link(
        hashid='test',
        url='http://google.com/test'
    )
    db_session.add(link)
    assert db_session.query(Link).filter(Link.url == 'http://google.com/test').count() == 1
    assert link._hash == sha1('http://google.com/test').hexdigest()
    # Testing the hashes attributes are created
    assert link._hash_path == sha1('google.com/test').hexdigest()
    assert link._hash_netloc == sha1('google.com').hexdigest()
    assert link._hash_netloc == sha1('google.com').hexdigest()


def test_create_link_with_user_id(db_session):
    link = Link(
        hashid='test',
        user_id=1,
        url='http://google.com/test'
    )
    db_session.add(link)
    assert db_session.query(Link.url == 'http://google.com/test').count() == 1


def test_create_link_without_user_id_unique_constraint(db_session):
    link_one = Link(
        hashid='hashone',
        url='http://google.com/test'
    )
    link_two = Link(
        hashid='hashtwo',
        url='http://google.com/test'
    )
    db_session.add(link_one)
    db_session.add(link_two)
    with pytest.raises(IntegrityError) as excinfo:
        db_session.flush()
    assert 'violates unique constraint "unique_url_and_user_id_is_null"' in str(excinfo.value)


def test_create_link_with_user_id_unique_constraint(db_session):
    link_one = Link(
        hashid='hashone',
        user_id=1,
        url='http://google.com/test'
    )
    link_two = Link(
        hashid='hashtwo',
        user_id=1,
        url='http://google.com/test'
    )
    db_session.add(link_one)
    db_session.add(link_two)
    with pytest.raises(IntegrityError) as excinfo:
        db_session.flush()
    assert 'violates unique constraint "unique_url_and_user_id"' in str(excinfo.value)


def test_link_hashid_not_null_contraint(db_session):
    link = Link(url='http://google.com/test')
    db_session.add(link)
    with pytest.raises(IntegrityError) as excinfo:
        db_session.flush()
    assert 'violates not-null constraint' in str(excinfo.value)


def test_link_url_not_null_constraint(db_session):
    link = Link(hashid='12345')
    db_session.add(link)
    with pytest.raises(IntegrityError) as excinfo:
        db_session.flush()
    assert 'violates not-null constraint' in str(excinfo.value)
