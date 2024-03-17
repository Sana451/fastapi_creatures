from error import Missing, Duplicate
from .init import conn, curs, IntegrityError
from model.explorer import Explorer

CREATE_TABLE = """create table if not exists explorer(
                name text primary key,
                country text,
                description text)"""

curs.execute(CREATE_TABLE)
print(CREATE_TABLE)


def row_to_model(row: tuple) -> Explorer:
    name, country, description = row
    return Explorer(name=name, country=country, description=description)


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump() if explorer else None


def get_one(name: str) -> Explorer:
    query = "select * from explorer where name=:name"
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def get_all() -> list[Explorer]:
    query = "select * from explorer"
    curs.execute(query)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    query = """insert into explorer values
                (:name, :country, :description)"""
    params = model_to_dict(explorer)
    try:
        curs.execute(query, params)
        conn.commit()
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists")
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    query = """update explorer set 
                    name=:name,
                    country=:country,
                    description=:description
                where name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = name
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists")
    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def update(name: str, explorer: Explorer):
    pass


def delete(name: str):
    query = "delete from explorer where name=:name"
    params = {"name": name}
    res = curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found")
