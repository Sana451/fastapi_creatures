from error import Missing, Duplicate
from model.user import User
from .init import conn, curs, IntegrityError

CREATE_TABLE_USER = """create table if not exists
                user(
                  name text primary key,
                  hash text)"""
curs.execute(CREATE_TABLE_USER)
print(CREATE_TABLE_USER)

CREATE_TABLE_XUSER = """create table if not exists
                xuser(
                  name text primary key,
                  hash text)"""
curs.execute(CREATE_TABLE_XUSER)
print(CREATE_TABLE_XUSER)


def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> dict:
    return user.model_dump() if user else None


def get_one(name: str) -> User:
    query = "select * from user where name=:name"
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found")


def get_all() -> list[User]:
    query = "select * from user"
    curs.execute(query)
    return [row_to_model(row) for row in curs.fetchall()]


def create(user: User, table: str = "user"):
    if table not in ("user", "xuser"):
        raise Exception(f"Invalid table name {table}")
    query = f"""insert into {table}
            (name, hash)
            values
            (:name, :hash)"""
    params = model_to_dict(user)
    try:
        curs.execute(query, params)
        conn.commit()
    except IntegrityError:
        raise Duplicate(msg=f"{table}: user {user.name} already exists")
    return user


def modify(name: str, user: User) -> User:
    query = """update user set
                    name=:name,
                    hash=:hash
                where name=:name0"""
    params = model_to_dict(user)
    params["name0"] = name
    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {name} not found")


def delete(name: str):
    user = get_one(name)
    query = "delete from user where name=:name"
    params = {"name": name}
    curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"User {name} not found")
    create(user, table="xuser")
