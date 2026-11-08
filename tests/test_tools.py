"""ツールのテスト（LLMもAPIキーも使わない）。"""

import json

from app import tools


def test_glossary_ids_are_unique_and_related_links_exist():
    terms = tools.load_glossary()
    ids = [t["id"] for t in terms]
    assert len(ids) == len(set(ids))
    for t in terms:
        for r in t["related"]:
            assert r in ids, f"{t['id']} の related に存在しない id: {r}"


def test_search_finds_term_by_name_and_alias():
    for query in ["LoRA", "lora", "Low-Rank Adaptation"]:
        hits = json.loads(tools.search_glossary(query))
        assert hits[0]["term"] == "LoRA", query


def test_search_finds_course_specific_term():
    hits = json.loads(tools.search_glossary("lecNN-start"))
    assert hits[0]["term"] == "lecNN-start タグ"


def test_search_limits_number_of_results():
    hits = json.loads(tools.search_glossary("エージェント"))
    assert 1 <= len(hits) <= tools.MAX_RESULTS


def test_search_reports_not_found():
    assert "見つかりませんでした" in tools.search_glossary("存在しない用語xyz")


def test_lecture_summary():
    assert "エージェント" in tools.get_lecture_summary(3)
    assert "まだありません" in tools.get_lecture_summary(99)


def test_make_quiz_returns_four_choices_and_the_correct_answer():
    terms = [term for term in tools.load_glossary() if term["lecture"] == 2]

    quiz = json.loads(tools.make_quiz(2))

    assert quiz["question"].startswith("「")
    assert quiz["question"].endswith("」の意味は？")
    assert len(quiz["choices"]) == 4
    assert [choice["label"] for choice in quiz["choices"]] == list("ABCD")
    correct_choice = next(choice for choice in quiz["choices"] if choice["label"] == quiz["answer"])
    assert any(
        quiz["question"] == f"「{term['term']}」の意味は？"
        and correct_choice["text"] == term["definition"]
        for term in terms
    )
    assert len({choice["text"] for choice in quiz["choices"]}) == 4


def test_make_quiz_reports_when_lecture_has_no_terms():
    assert "第0回の用語が見つかりませんでした。" == tools.make_quiz(0)


def test_save_learning_log_writes_topic_and_note(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path / "learning_log")

    message = tools.save_learning_log("用語の復習", "LoRAについて学んだ")

    files = list(tools.LOG_DIR.glob("*.json"))
    assert len(files) == 1
    assert json.loads(files[0].read_text(encoding="utf-8")) == {
        "topic": "用語の復習",
        "note": "LoRAについて学んだ",
    }
    assert message == f"保存しました: {files[0].name}"


def test_default_question_of_lecture1_is_answerable_from_glossary():
    """第1回の既定の質問（app.ask）は、第3回のエージェントが用語集で正しく答えられること。"""
    from app.ask import DEFAULT_QUESTION

    assert "3レベル" in DEFAULT_QUESTION
    hits = json.loads(tools.search_glossary("3レベル"))
    assert hits[0]["term"] == "宿題の3レベル"
