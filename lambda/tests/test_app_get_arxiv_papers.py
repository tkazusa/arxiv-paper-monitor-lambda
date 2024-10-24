import datetime

from src.app import get_arxiv_papers, is_relevant_to_interest


def test_get_arxiv_papers_constructs_correct_date_range(mocker):
    """Test that the correct date range is used in the arXiv query."""
    
    # Mock datetime.now()
    mocker.patch("datetime.datetime", **{
        "now.return_value": datetime.datetime(2024, 10, 20)
    })

    # Mock the arxiv.Client
    mock_client = mocker.patch('arxiv.Client')
    mock_client_instance = mock_client.return_value
    mock_client_instance.results.return_value = []

    # Mock the arxiv.Search
    mock_search = mocker.patch('arxiv.Search')

    # Call the function
    get_arxiv_papers()

    # Assert that the correct query was used
    expected_date_range = '[20241019 TO 20241020]'
    search_args, search_kwargs = mock_search.call_args
    assert search_kwargs['query'] == expected_date_range
