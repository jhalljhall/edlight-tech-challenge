from typing import Any, List, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Form

#? is this just for user authentication?
#from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
# from database import SessionLocal, engine

from app import models, schemas, controllers
from app.api import deps
from app.core.config import settings

router = APIRouter()

'''
TODO:
- get - read all drinks as anonymous user
- post - create new drink (dev)
- put - update drink (dev)
- get - my favorite/saved-to-list drinks ------ #? is this included in lists instead
- get - get specific drinks by id as anonymous user
- get - read all drinks as authorized user
- get - get specific drink by id as authorized user
'''

#!- get - read all drinks as anonymous user
@router.get("/", response_model=List[schemas.Drink])
def read_drink(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
#   current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    drinks = controllers.drink.get_multi(db, skip=skip, limit=limit)
    return drinks

#!- post - create new business (dev)
@router.post("/", response_model=schemas.Drink)
def create_drink(
    *,
    db: Session = Depends(deps.get_db),
    drink_in: schemas.DrinkBase,
#    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    new_drink = controllers.drink.create_drink(db, obj_in=drink_in)
    return new_drink
