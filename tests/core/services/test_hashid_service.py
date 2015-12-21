def test_encode(hashid_svc):
    hashid = hashid_svc.encode(1)
    assert len(hashid) >= 6


def test_decode(hashid_svc):
    primary_id = 10
    hashid = hashid_svc.encode(primary_id)
    assert hashid_svc.decode(hashid) == (primary_id,)


def test_encode_with_secondary_id(hashid_svc):
    hashid1 = hashid_svc.encode(1)
    assert len(hashid1) >= 6
    hashid2 = hashid_svc.encode(1, 2)
    assert len(hashid2) >= 6
    hashid1 != hashid2


def test_decode_with_secondary_id(hashid_svc):
    primary_id = 10
    secondary_id = 5
    hashid = hashid_svc.encode(primary_id, secondary_id)
    assert hashid_svc.decode(hashid) == (primary_id, secondary_id)
