from suma.core.services.interfaces import IHashIdService
from zope.interface import implementer
from structlog import get_logger
log = get_logger()
import hashids


@implementer(IHashIdService)
class HashIdService(object):
    def __init__(self, secret):
        self.hashids = hashids.Hashids(secret, min_length=6)

    def encode(self, primary_id, secondary_id=None):
        args = []
        if secondary_id is not None:
            # Using the primary_id as 1st argument create better entropy
            # The same user with different link will get very different ids
            args.append(secondary_id)
        args.append(primary_id)
        return self.hashids.encode(*args)

    def decode(self, short_id):
        # we are reversing the order to respect primary first in the return
        return self.hashids.decode(short_id)[::-1] # we use the step to ensure a tuple
