import os
import string
from collections import Counter

from fastapi import APIRouter, HTTPException, status, Response
import plotly.express as px
import country_converter as coco

from error import Missing, Duplicate
from model.creature import Creature
from service.creature import get_all

if os.getenv("CRYPTID_UNIT_TEST"):
    import fake.creature as service
else:
    import service.creature as service

router = APIRouter(prefix="/creature")


@router.get("/plot")
def plot():
    creatures = get_all()

    letters = string.ascii_uppercase
    counts = Counter(creature.name[0] for creature in creatures)
    y = {letter: counts.get(letter, 0) for letter in letters}

    fig = px.histogram(x=list(letters), y=y,
                       title="Creature Names",
                       labels={"x": "Initial", "y": "Initial"})
    fig_bytes = fig.to_image(format="png")

    return Response(content=fig_bytes, media_type="image/png")


@router.get("/map")
def map():
    creatures = service.get_all()
    iso2_codes = set(creature.country for creature in creatures)
    iso3_codes = coco.convert(names=iso2_codes, to="ISO3")
    fig = px.choropleth(
        locationmode="ISO-3",
        locations=iso3_codes)
    fig_bytes = fig.to_image(format="png")
    print(iso2_codes)
    print(iso3_codes)
    return Response(content=fig_bytes, media_type="image/png")


@router.get("")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Creature | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


@router.post("", status_code=status.HTTP_201_CREATED)
def create(explorer: Creature) -> Creature:
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature:
    try:
        return service.modify(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


@router.put("/{name}")
def replace(creature: Creature) -> Creature:
    return service.replace(creature)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)
