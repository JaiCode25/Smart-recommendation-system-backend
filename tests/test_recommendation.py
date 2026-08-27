"""Unit tests for end-to-end recommendation engine scoring and explainability."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import app.models  # load all mappers
from app.database import Base
from app.models.user import User
from app.models.item import Item, ItemTag
from app.models.tag import Tag
from app.models.interaction import Interaction
from app.graph.tag_graph import tag_graph_engine
from app.recommendation.engine import RecommendationEngine


def test_recommendation_engine_scoring_and_ranking():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    user = User(id=1, username="recsys_tester")
    db.add(user)

    t_crick = Tag(id=1, name="cricket")
    t_bat = Tag(id=2, name="batting")
    t_py = Tag(id=3, name="python")
    db.add_all([t_crick, t_bat, t_py])
    db.flush()

    tag_graph_engine.graph.clear()
    tag_graph_engine.add_edge("cricket", "batting", weight=0.95)

    item_relevant = Item(
        id=1, item_id="item-crick", source="youtube", title="Virat Batting", url="http://a", category="sports"
    )
    item_unrelated = Item(
        id=2, item_id="item-py", source="youtube", title="Python Guide", url="http://b", category="programming"
    )
    db.add_all([item_relevant, item_unrelated])
    db.flush()

    db.add(ItemTag(item_id=1, tag_id=1))
    db.add(ItemTag(item_id=1, tag_id=2))
    db.add(ItemTag(item_id=2, tag_id=3))

    db.add(Interaction(user_id=1, item_id=1, interaction_type="like", weight=5.0))
    db.commit()

    recs_engine = RecommendationEngine(db)
    recs = recs_engine.generate_recommendations(user_id=1, limit=5, include_consumed=True)

    assert len(recs) == 2
    assert recs[0].item.id == 1
    assert recs[0].score > recs[1].score
    assert recs[0].explanation.summary is not None
    assert "cricket" in recs[0].explanation.direct_matching_tags

    db.close()
