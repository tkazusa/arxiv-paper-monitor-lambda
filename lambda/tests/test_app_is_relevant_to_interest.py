import pytest
import os

from src.app import is_relevant_to_interest

# Test case for missing API key
def test_no_api_key(mocker):
    """
    Test that the function raises a ValueError when the API key is missing.
    """
    # Mock the environment variable to simulate missing API key
    mocker.patch.dict(os.environ, {}, clear=True)

    with pytest.raises(ValueError):
        is_relevant_to_interest("This is a paper about AI.", "artificial intelligence")

# Test case for handling API errors
def test_api_error_handling(mocker):
    """
    Test that the function returns False when an error occurs during the API call.
    """
    mock_client = mocker.patch('src.app.arxiv.Client')
    # Mock OpenAI Completion.create to raise an exception
    mock_openai_client = mocker.patch('openai.completions.create')
    mock_openai_client.side_effect = Exception("API call failed")

    # Mock environment variable for the API key
    mocker.patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})

    result = is_relevant_to_interest("This is a paper about data science.", "data science")

    # Assert that the function handles the error and returns False
    assert result is False
