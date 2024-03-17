import os

import pytest
from model.creature import Creature
from error import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import creature as data


@pytest.fixture
def sample_creature() -> Creature:
    return Creature(name="yeti", country="CN", area="Himalayas", description="Harmless Himalayan",
                    aka="Abominable Snowman")


def test_create(sample_creature):
    resp = data.create(sample_creature)
    assert resp == sample_creature


def test_create_duplicate(sample_creature):
    with pytest.raises(Duplicate):
        _ = data.create(sample_creature)


def test_get_one(sample_creature):
    resp = data.get_one(sample_creature.name)
    assert resp == sample_creature


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = data.get_one("boxturtle")


def test_modify(sample_creature):
    sample_creature.area = "Sesame Street"
    resp = data.modify(sample_creature.name, sample_creature)
    assert resp.area == "Sesame Street"
    assert resp == sample_creature


def test_modify_missing():
    thing: Creature = Creature(name="snuffle", country="RU", area="", description="some thing", aka="")
    with pytest.raises(Missing):
        _ = data.modify(thing.name, thing)


def test_delete(sample_creature):
    resp = data.delete(sample_creature.name)
    assert resp is None


def test_delete_missing(sample_creature):
    with pytest.raises(Missing):
        _ = data.delete(sample_creature.name)
