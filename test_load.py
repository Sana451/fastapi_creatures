from faker import Faker
from time import perf_counter


def load(num=100_000):
    from error import Duplicate
    from data.explorer import create
    from model.explorer import Explorer

    f = Faker()
    t1 = perf_counter()
    for row in range(num):
        try:
            create(
                Explorer(
                    name=f.name(),
                    country=f.country(),
                    description=f.description
                ))
        except Duplicate:
            pass

    t2 = perf_counter()
    print(num, "rows")
    print("write time: ", t2 - t1)


def read_db():
    from data.explorer import get_all

    t1 = perf_counter()
    _ = get_all()
    t2 = perf_counter()
    print("db read time: ", t2 - t1)


def read_api():
    from fastapi.testclient import TestClient
    from main import app

    t1 = perf_counter()
    client = TestClient(app)
    _ = client.get("/explorer/")
    t2 = perf_counter()
    print("api read time: ", t2 - t1)


load()
read_db()
read_db()
read_api()
