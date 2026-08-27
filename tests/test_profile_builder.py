"""Unit tests for dynamic user interest profile generation with decay."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import app.models  # load all mappers
from app.database import Base
from app.models.user import User
from app.models.item import Item, ItemTag
from app.models.tag import Tag
from app.models.interaction import Interaction
from app.recommendation.profile_builder import UserProfileBuilder


def test_user_profile_calculation():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    user = User(id=1, username="tester")
    db.add(user)

    item1 = Item(id=1, item_id="item-1", source="youtube", title="Cricket Item", url="http://test", category="sports")
    item2 = Item(id=2, item_id="item-2", source="youtube", title="Disliked Item", url="http://test", category="tech")
    db.add_all([item1, item2])
    db.flush()

    tag_crick = Tag(id=1, name="cricket")
    tag_bad = Tag(id=2, name="spam")
    db.add_all([tag_crick, tag_bad])
    db.flush()

    db.add(ItemTag(item_id=1, tag_id=1))
    db.add(ItemTag(item_id=2, tag_id=2))

    db.add(Interaction(user_id=1, item_id=1, interaction_type="like", weight=5.0))
    db.add(Interaction(user_id=1, item_id=2, interaction_type="dislike", weight=-5.0))
    db.commit()

    pos_interests, neg_penalties = UserProfileBuilder.calculate_direct_interests(db, user_id=1)
    
    assert "cricket" in pos_interests
    assert pos_interests["cricket"] > 0
    assert "spam" in neg_penalties
    assert neg_penalties["spam"] > 0

    db.close()
