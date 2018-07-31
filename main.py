import json
import requests
import os
from urllib.parse import unquote

def authorized(question):
  if 'token' in question and question['token'] == os.environ['SECRET']:
    return True
  else:
    return False
  
def valid(question):
  if question == None:
    return False
  if question and 'text' in question:
    return True
  else:
    return False
  
def parse_slack_text(text):
  clean = ' '.join(text.split('+'))
  return unquote(clean)
  
def request_to_dict(request_data):
  body = {}
  for line in request_data.decode().split('&'):
    arr = line.split('=')
    body[arr[0]] = arr[1]
  return body


def process(question):
  # question_text = question['text']  # no parsing
  question_text = parse_slack_text(question['text'])

  answer = {'text': 'I do not have an answer for ya. Try pressing harder on the enter key.'}
  
  r = requests.post(os.environ['LOG_SERVICE'], json={"user":question['user_name'], "action": question_text})
  if r.status_code == requests.codes.ok:
    answer = {'text' : r.json()['status']}
  else:
    answer = {'text' : 'Error: failed to send log to external api. remote error: ' + r.json()['status'] }
  return json.dumps(answer)
  
  
def run(request):
  question = request_to_dict(request.get_data())
  # return json.dumps({"text":str(question)})

  # Validate and authorized
  if not valid(question):
    return json.dumps({"text":'Something when wrong. Sorry!'})
  if not authorized(question):
    return json.dumps({"text":'You are not authorized to do that'})
  
  # Process and reply
  return process(question)
