"""Unit tests for tag normalization and text extraction."""
from app.tagging.normalizer import normalize_tag, normalize_tag_list
from app.tagging.extractor import extract_tags_from_text


def test_normalize_single_tag():
    assert normalize_tag("  Cricket  ") == "cricket"
    assert normalize_tag("Virat_Kohli") == "virat-kohli"
    assert normalize_tag("Machine Learning 101!") == "machine-learning-101"
    assert normalize_tag("---sports---") == "sports"
    assert normalize_tag("") == ""


def test_normalize_tag_list_deduplication_and_stopwords():
    raw_tags = ["cricket", "CRICKET", "the", "a", "batting", "virat kohli", "with"]
    normalized = normalize_tag_list(raw_tags)
    assert normalized == ["cricket", "batting", "virat-kohli"]
    assert "the" not in normalized
    assert "a" not in normalized


def test_extract_tags_from_text():
    title = "Virat Kohli Masterclass: Perfecting the Cover Drive & Batting Stance"
    desc = "Learn batting technique and international cricket tactics."
    tags = extract_tags_from_text(title, desc, category="sports")
    assert "cricket" in tags
    assert "virat-kohli" in tags
    assert "batting" in tags
    assert "sports" in tags
