from exceptions import InternalException
from constants import FlagColor, CBI_FLAG_COLOR_ENDPOINT
from ddb import put_flag_color, get_last_flag_color
from exceptions import ClientException
from sns import publish_flag_change_notification

from datetime import datetime, timezone

import requests

def main(event, context):
  try:
    print(f'Invocation with Event: {event}; Context {context}')
    if event.get('source') == "aws.events":
      handle_eventbridge_invocation()
    elif event.get('flag_color'):
      return handle_api_invocation(event.get('flag_color'))
    else:
      raise ClientException('Unknown invocation method')
  except ClientException as e:
    print(e)
    raise ClientException(f'ClientException: {str(e)}')
  except InternalException as e:
    print(e)
    raise InternalException('Internal server error.')
  except Exception as e:
    print(e)
    raise InternalException('Internal server error.')


def handle_api_invocation(received_flag_color):
  print('Event body contains color - defaulting to APIG')
  try:
    received_flag_color = FlagColor(received_flag_color)
    if received_flag_color in [FlagColor.GREEN, FlagColor.YELLOW, FlagColor.RED]:
      current_timestamp_utc = datetime.now(timezone.utc)
      put_flag_color(received_flag_color, current_timestamp_utc)
      publish_flag_change_notification(received_flag_color, current_timestamp_utc)
      return {
        'success': 'true',
        'flag_color': received_flag_color.value
      }
    else:
      raise ValueError
  except ValueError:
    raise ClientException(f'{received_flag_color} is not a valid flag color')


def handle_eventbridge_invocation():
  print('Event body comes from EventBridge.')
  try:
    current_flag_color = get_current_flag_color()
    if current_flag_color == FlagColor.CLOSED:
      print(f'Current flag color is C which means CBI is closed. Ignoring.')
      return
    last_flag_color = get_last_flag_color()
    if current_flag_color == last_flag_color:
      print(f'Current and last flag colors received are the same. Ignoring.')
      return
    else:
      current_timestamp_utc = datetime.now(timezone.utc)
      put_flag_color(current_flag_color, current_timestamp_utc)
      publish_flag_change_notification(current_flag_color, current_timestamp_utc)
  except Exception as e:
    print(e)
    raise InternalException()


def get_current_flag_color():
  try:
    response_text = requests.get(CBI_FLAG_COLOR_ENDPOINT).text
    # Returns in format 'var FLAG_COLOR = "?"' where ? in ['C', 'G', 'Y', 'R']
    color_str = response_text.split(' ')[-1][1]
    print(f'Got current flag color from CBI: {color_str}')
    return FlagColor(color_str)
  except Exception as e:
    print(e)
    raise InternalException()


if __name__ == "__main__":   
  main('', '')