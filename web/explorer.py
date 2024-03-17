from fastapi import APIRouter, HTTPException
from fastapi import status
from model.explorer import Explorer
# import fake.explorer as service
import service.explorer as service
from error import Duplicate, Missing

router = APIRouter(prefix="/explorer")


@router.get("")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Explorer:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


@router.post("", status_code=status.HTTP_201_CREATED)
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


@router.patch("/{name}")
def modify(name: str, explorer: Explorer) -> Explorer:
    try:
        return service.modify(name, explorer)
    except (Missing, Duplicate) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


@router.put("/{name}")
def replace(name: str, explorer: Explorer) -> Explorer:
    return service.replace(name, explorer)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)
