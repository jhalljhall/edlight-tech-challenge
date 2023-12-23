from typing import Any, List, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Form

#? is this just for user authentication?
#from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
# from database import SessionLocal, engine

from app import models, schemas, controllers
#? from app.controllers import BusinessController
#? tried to import business from the controller??????
from app.controllers.BusinessController import business

from app.api import deps
from app.core.config import settings

router = APIRouter()

'''
TODO:
- get - read all businesses as anonymous user
- post - create new business (dev)
- put - update business (dev)
- get - my favorite businesses ------ #? is this included in lists instead
- get - get specific business by id as anonymous user
- get - read all businesses as authorized user
- get - get specific business by id as authorized user
'''

#!- get - read all businesses as anonymous user
@router.get("/", response_model=List[schemas.Business])
def read_businesses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
#   current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    businesses = controllers.business.get_multi(db, skip=skip, limit=limit)
    return businesses

#!- post - create new business (dev)
@router.post("/", response_model=schemas.Business)
def create_business(
    *,
    db: Session = Depends(deps.get_db),
    business_in: schemas.BusinessBase,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    business_exists = controllers.business.get_business_by_name(db, name=business_in.name)
    if business_exists:
        raise HTTPException(
            status_code=400,
            detail="The business with this name already exists in the system.",
        )
    new_business = controllers.business.create(db, obj_in=business_in)
    return new_business
