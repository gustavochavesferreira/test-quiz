import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct






def test_rejects_choice_with_invalid_text():
    question = Question(title='q1')

    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')
    with pytest.raises(Exception,match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)

    assert question.choices == []


def test_removes_choice_with_existing_id():
    question = Question(title='q1')
    removed_choice = question.add_choice('a')
    remaining_choice = question.add_choice('b')

    question.remove_choice_by_id(removed_choice.id)

    assert question.choices == [remaining_choice]


def test_rejects_removal_with_unknown_choice_id():
    question = Question(title='q1')
    choice = question.add_choice('a')

    with pytest.raises(Exception, match='Invalid choice id 999'):
        question.remove_choice_by_id(999)

    assert question.choices == [choice]


def test_removes_all_five_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')
    question.add_choice('e')

    question.remove_all_choices()

    assert question.choices == []


def test_creates_choices_as_incorrect_by_default():
    question = Question(title='q1')

    first_choice = question.add_choice('a')
    second_choice = question.add_choice('b')

    assert first_choice.is_correct is False
    assert second_choice.is_correct is False


def test_marks_only_requested_choices_as_correct():
    question = Question(title='q1')
    first_correct_choice = question.add_choice('a')
    incorrect_choice = question.add_choice('b')
    second_correct_choice = question.add_choice('c')

    question.set_correct_choices([first_correct_choice.id, second_correct_choice.id])

    assert first_correct_choice.is_correct is True
    assert incorrect_choice.is_correct is False
    assert second_correct_choice.is_correct is True


def test_returns_empty_list_when_all_selected_choices_are_incorrect():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    first_incorrect_choice = question.add_choice('b', False)
    second_incorrect_choice = question.add_choice('c', False)

    result = question.correct_selected_choices([first_incorrect_choice.id,second_incorrect_choice.id])

    assert result == []


def test_ignores_unknown_id_when_correcting_selected_choices():
    question = Question(title='q1')
    question.add_choice('a', True)

    result = question.correct_selected_choices([999])

    assert result == []


def test_rejects_unknown_id_when_setting_correct_choices():
    question = Question(title='q1')
    choice = question.add_choice('a')

    with pytest.raises(Exception, match='Invalid choice id 999'):
        question.set_correct_choices([999])

    assert choice.is_correct is False


def test_rejects_more_selections_than_allowed():
    question = Question(title='q1', max_selections=2)
    first_choice = question.add_choice('a')
    second_choice = question.add_choice('b')
    third_choice = question.add_choice('c')

    with pytest.raises(Exception, match='Cannot select more than 2 choices'):
        question.correct_selected_choices([first_choice.id, second_choice.id, third_choice.id])

@pytest.fixture
def question_with_correct_and_incorrect_choices():
    question = Question(title='q1', max_selections=2)
    correct_choice_1 = question.add_choice('a', True)
    correct_choice_2 = question.add_choice('b', True)
    incorrect_choice = question.add_choice('c', False)
    return question, correct_choice_1, correct_choice_2, incorrect_choice


def test_returns_all_selected_correct_choice_ids(question_with_correct_and_incorrect_choices):
    question, correct_choice_1, correct_choice_2, _ = (question_with_correct_and_incorrect_choices)

    result = question.correct_selected_choices([correct_choice_1.id,correct_choice_2.id])

    assert result == [correct_choice_1.id, correct_choice_2.id]


def test_returns_only_correct_choice_ids_from_mixed_selection(
    question_with_correct_and_incorrect_choices
):
    question, correct_choice, _, incorrect_choice = (question_with_correct_and_incorrect_choices)

    result = question.correct_selected_choices([correct_choice.id, incorrect_choice.id])

    assert result == [correct_choice.id]