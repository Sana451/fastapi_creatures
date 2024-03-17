import os
import pytest
from model.explorer import Explorer
from error import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import explorer as data


@pytest.fixture
def sample_explorer() -> Explorer:
    return Explorer(name="sana", country="ru", description="Developer")


def test_get_all_start():
    assert len(data.get_all()) == 0


def test_create(sample_explorer):
    resp = data.create(sample_explorer)
    assert resp == sample_explorer


def test_create_duplicate(sample_explorer):
    with pytest.raises(Duplicate):
        _ = data.create(sample_explorer)


def test_get_all_one():
    assert len(data.get_all()) == 1


def test_get_one(sample_explorer):
    resp = data.get_one(sample_explorer.name)
    assert resp == sample_explorer


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = data.get_one("boxturtle")


def test_modify(sample_explorer):
    sample_explorer.country = "usa"
    resp = data.modify(sample_explorer.name, sample_explorer)
    assert resp.country == "usa"
    assert resp == sample_explorer


def test_modify_missing():
    thing: Explorer = Explorer(name="", country="RU", description="qwerty")
    with pytest.raises(Missing):
        _ = data.modify(thing.name, thing)


def test_delete(sample_explorer):
    resp = data.delete(sample_explorer.name)
    assert resp is None


def test_delete_missing(sample_explorer):
    with pytest.raises(Missing):
        _ = data.delete(sample_explorer.name)
