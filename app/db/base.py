# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User, UserBadge, UserTag, UserInDB  # noqa
from app.models.token import Token  # noqafrom .user import User, UserBadge, UserTag
from app.models.tag import Tag
from app.models.review import Review
from app.models.drink import Drink
from app.models.collection_tracker import Collection, CollectionTrackerBadge, CollectionTrackerDrink
from app.models.business import Business, BusinessTag
from app.models.badge import Badge
