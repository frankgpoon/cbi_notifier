from constants import FlagColor
from constants import NOTIFIER_SNS_TOPIC_ARN
from exceptions import handle_botocore_error, InternalException

from datetime import datetime
import json

import botocore
import boto3
from pytz import timezone

sns_client = boto3.client('sns')

def publish_flag_change_notification(flag_color, timestamp_utc):
  try:
    print('Publishing SNS message')
    sns_client.publish(
      TopicArn=NOTIFIER_SNS_TOPIC_ARN,
      Message=json.dumps({
        'default': 'default response',
        'email': format_basic_response(flag_color, timestamp_utc),
        'sms': 'sms response'
      }),
      Subject='Community Boating Flag Change Notification',
      MessageStructure='json',
      MessageAttributes={
          'flag_color': {
            'DataType': 'String',
            'StringValue': flag_color.value,
          },
          'timestamp_utc': {
            'DataType': 'String',
            'StringValue': timestamp_utc.isoformat()
          }
      }
    )
  except botocore.exceptions.ClientError as e:
    handle_botocore_error(e)
  except Exception as e:
    print(e)
    raise InternalException()


def format_basic_response(flag_color, timestamp_utc):
  formatted_flag_color = flag_color.name.lower()
  timestamp_eastern = timestamp_utc.astimezone(timezone('US/Eastern'))
  formatted_timestamp = timestamp_eastern.strftime('%A, %B %d, %Y at %I:%M%p')

  return ('This is a message to tell you that the flag color at Community ' 
    + 'Boating has changed. The new color is {}. \n\nThe new flag color ' 
    + 'is up to date as of {}.').format(formatted_flag_color, 
    formatted_timestamp)