import arxiv
import datetime

from typing import Generator

def get_arxiv_papers() -> Generator[arxiv.Result, None, None]:
  """ Get the 500 most recent papers from arXiv.
  """
  # Get the date range for the query.
  now = datetime.datetime.now()
  yesterday = now - datetime.timedelta(days=1)
  date_range = f'[{yesterday.strftime("%Y%m%d")} TO {now.strftime("%Y%m%d")}]'
  
  # Construct the default API client.
  client = arxiv.Client()

  # Search for the 10 most recent articles matching the keyword "quantum."
  search = arxiv.Search(
    query = date_range,
    max_results = 500,
    sort_by = arxiv.SortCriterion.SubmittedDate
  )

  return client.results(search)
