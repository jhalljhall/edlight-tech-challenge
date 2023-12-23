from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, businesses, drinks, tags, reviews, collections
#collections

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(businesses.router, prefix="/businesses", tags=["businesses"])
api_router.include_router(drinks.router, prefix="/drinks", tags=["drinks"])
api_router.include_router(collections.router, prefix="/collections", tags=["collections"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
