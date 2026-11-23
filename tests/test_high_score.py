import json

from logic_utils import closeness_percent, load_high_scores, record_high_score


def test_missing_file_returns_empty(tmp_path):
    assert load_high_scores(str(tmp_path / "nope.json")) == {}


def test_first_score_is_a_record_and_is_saved(tmp_path):
    path = str(tmp_path / "hs.json")
    assert record_high_score("Normal", 70, path) == (True, 70)
    assert load_high_scores(path) == {"Normal": 70}


def test_lower_or_equal_score_does_not_replace_best(tmp_path):
    path = str(tmp_path / "hs.json")
    record_high_score("Normal", 70, path)
    assert record_high_score("Normal", 50, path) == (False, 70)
    assert record_high_score("Normal", 70, path) == (False, 70)
    assert load_high_scores(path) == {"Normal": 70}


def test_higher_score_replaces_best_and_difficulties_are_separate(tmp_path):
    path = str(tmp_path / "hs.json")
    record_high_score("Easy", 40, path)
    assert record_high_score("Easy", 80, path) == (True, 80)
    record_high_score("Hard", 10, path)
    assert load_high_scores(path) == {"Easy": 80, "Hard": 10}


def test_corrupt_or_wrong_shape_file_is_ignored(tmp_path):
    path = tmp_path / "hs.json"
    path.write_text("{not json")
    assert load_high_scores(str(path)) == {}
    path.write_text(json.dumps([1, 2, 3]))
    assert load_high_scores(str(path)) == {}
    path.write_text(json.dumps({"Easy": "lots", "Hard": 5, "Normal": True}))
    assert load_high_scores(str(path)) == {"Hard": 5}


def test_negative_best_can_be_beaten(tmp_path):
    path = str(tmp_path / "hs.json")
    record_high_score("Hard", -15, path)
    assert record_high_score("Hard", -5, path) == (True, -5)


def test_unwritable_path_does_not_crash(tmp_path):
    bad_path = str(tmp_path / "no_dir" / "x.json")
    assert record_high_score("Easy", 5, bad_path) == (True, 5)


def test_closeness_percent():
    assert closeness_percent(50, 50, 1, 100) == 100
    assert closeness_percent(1, 100, 1, 100) == 0
    assert 0 <= closeness_percent(500, 1, 1, 100) <= 100
