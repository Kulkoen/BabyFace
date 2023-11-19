import re
# from helper import *
from database import *
from sendblue import *


# only gets the first link?
def get_links(string):
  # Use a regular expression to find all links in the string
  links = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", string)

  # user didn't input a link
  # TODO: give a regular response
  if len(links) == 0:
    raise Exception("No link in message")
  
  return links[0]

def handle_message(phoneId, message):
  # cooldown post article
  check_timestamp(phoneId)

  # Limits the number of requests per user based on their subscription
  check_request_count(phoneId)
  
  # get links
  link = get_links(message)
  
  # checking timestamp
  update_user_timestamp(phoneId)

  # Removed specific website checks and related function calls
  raise Exception("Unknown Link Type")