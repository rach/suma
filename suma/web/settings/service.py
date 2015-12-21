from suma.common.services import (
    link_service_factory,
    task_service_factory,
    hashid_service_factory,
    file_service_factory
)
from sqlalchemy import engine_from_config
from suma.core.models.meta import (
    create_dbsession
)
import zope.sqlalchemy


def includeme(config):
    engine = engine_from_config(config.registry.settings, 'sqlalchemy.')
    dbsession = create_dbsession(engine)
    zope.sqlalchemy.register(dbsession, keep_session=True)

    config.register_service(
        dbsession,
        name='db'
    )

    config.register_service_factory(
        link_service_factory,
        name='link'
    )

    # Needed just to initialize the link_service
    config.register_service_factory(
        hashid_service_factory,
        name='hashid'
    )

    config.register_service_factory(
        task_service_factory,
        name='task'
    )

    config.register_service_factory(
        file_service_factory,
        name='file'
    )
