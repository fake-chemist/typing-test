import pytest
from TypingTimer import TypingTest

@pytest.fixture
def typing_test():
    """Fixture to initialize the TypingTest instance."""
    test_instance = TypingTest()
    test_instance.testing_words = ["test", "word", "typing"]  # Set predefined words
    return test_instance

def test_word_picker(typing_test):
    """Test word_picker functionality."""
    typing_test.word_picker()
    assert typing_test.current_word == "test"
    assert typing_test.testing_word_ending == ["test"]
    assert typing_test.testing_words == ["word", "typing"]

def test_word_picker_exhaustion(typing_test):
    """Test word_picker behavior when words are exhausted."""
    typing_test.testing_words = []
    with pytest.raises(ValueError, match="All words typed"):
        typing_test.word_picker()

def test_calculate_accuracy(typing_test):
    """Test calculate_accuracy functionality."""
    typing_test.testing_word_ending = ["hello", "world"]
    typing_test.user_typed_words = ["hello", "python"]
    accuracy = typing_test.calculate_accuracy()
    assert accuracy == 50.0  # One out of two words matches

def test_calculate_accuracy_empty_lists(typing_test):
    """Test calculate_accuracy when both lists are empty."""
    typing_test.testing_word_ending = []
    typing_test.user_typed_words = []
    accuracy = typing_test.calculate_accuracy()
    assert accuracy == 0.0

def test_reset_game(typing_test):
    """Test reset_game functionality."""
    typing_test.start_time = 12345  # Simulated start time
    typing_test.end_time = 12350  # Simulated end time
    typing_test.score = 10
    typing_test.user_typed_words = ["hello", "world"]

    typing_test.reset_game()

    assert typing_test.user_input == ""
    assert typing_test.score == 0
    assert len(typing_test.user_typed_words) == 0
    assert typing_test.time_remaining == typing_test.time_limit
    assert typing_test.start_time is not None
    assert typing_test.current_word in typing_test.testing_word_ending

