import os
import datetime
from typing import Generator
import re

import arxiv
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

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



def is_relevant_to_interest(summary: str, user_interests: str) -> bool:
    """
    Determines if a research paper's summary is relevant to the user's interests using OpenAI's GPT model.

    Args:
        summary (str): The summary of the research paper.
        user_interests (str): The user's interests as a string.

    Returns:
        bool: True if relevant, False otherwise.
    """
    try:
        # Load API key from environment variables for security
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set it as an environment variable.")
        
        client = OpenAI(api_key=api_key)
        
        # Construct the prompt
        prompt = (
            f"The following is a summary of a research paper:\n"
            f"\"{summary}\"\n\n"
            f"The user is interested in the following topics:\n"
            f"\"{user_interests}\"\n\n"
            "Does this paper align with the user's interests? Please answer with 'yes' or 'no'."
        )
        
        # ChatGPT API call
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=10,
            temperature=0,
            timeout=10
        )
        
        # Extracting the response and cleaning it up
        answer = response.choices[0].text.strip().lower()
        clean_answer = re.sub(r'[^a-z]', '', answer)
        
        # Return True for "yes" and False for "no"
        return clean_answer == "yes"
    
    except APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        return False
    
    except APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        return False
    
    except RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        return False