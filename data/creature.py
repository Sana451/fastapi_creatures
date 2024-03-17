from error import Duplicate, Missing
from .init import conn, curs, IntegrityError
from model.creature import Creature

CREATE_TABLE = """create table if not exists creature(
                name text primary key,
                description text,
                country text,
                area text,
                aka text)"""

curs.execute(CREATE_TABLE)
print(CREATE_TABLE)


def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(name=name, description=description, country=country, area=area, aka=aka)


def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump() if creature else None


def get_one(name: str) -> Creature:
    query = "select * from creature where name=:name"
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Creature {name} not found")


def get_all() -> list[Creature]:
    query = "select * from creature"
    curs.execute(query)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(creature: Creature):
    query = """insert into creature values
            (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    try:
        curs.execute(query, params)
        conn.commit()
    except IntegrityError:
        raise Duplicate(msg=f"Creature {creature.name} already exists")
    return get_one(creature.name)


def modify(name: str, creature: Creature) -> Creature:
    query = """update creature set
                    name=:name,
                    country=:country,
                    area=:area, 
                    description=:description,
                    aka=:aka
                where name=:name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = name
    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(creature.name)
    else:
        raise Missing(f"Creature {name} not found")


def replace(creature: Creature):
    return creature


def delete(name: str):
    query = "delete from creature where name=:name"
    params = {"name": name}
    curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Creature {name} not found")
