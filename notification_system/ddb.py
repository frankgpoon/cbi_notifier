from exceptions import InternalException, handle_botocore_error
from constants import FlagColor, FLAG_COLOR_HISTORY_DDB_TABLE, FLAG_COLOR_HISTORY_MOST_RECENT_INDEX

import uuid

import botocore
import boto3

ddb_client = boto3.client('dynamodb')

def get_last_flag_color():
  try:
    response = ddb_client.query(
      TableName=FLAG_COLOR_HISTORY_DDB_TABLE,
      IndexName=FLAG_COLOR_HISTORY_MOST_RECENT_INDEX,
      ScanIndexForward=False,
      Limit=1,
      KeyConditionExpression='valid = :valid',
      ExpressionAttributeValues={
        ':valid': {
          'N': '1'
        }
      }
    )

    if response.get('Count') == 0:
      print(f'Did not get the last flag color - the table might be empty.')
      return None
    else:
      flag_color = response.get('Items')[0].get('flag_color').get('S')
      print(f'Got the last flag color as {flag_color}')
      return FlagColor(flag_color)
  except botocore.exceptions.ClientError as e:
    handle_botocore_error(e)
  except Exception as e:
    print(e)
    raise InternalException()


def put_flag_color(flag_color, timestamp_utc):
  entry_id = uuid.uuid4().hex
  try:
    print(f'Putting new flag color {flag_color}')
    ddb_client.put_item(
      TableName=FLAG_COLOR_HISTORY_DDB_TABLE,
      Item={
        'id': {
          'S': entry_id,
        },
        'timestamp': {
          'S': timestamp_utc.isoformat()
        },
        'flag_color': {
          'S': flag_color.value,
        },
        'valid': {
          'N': '1'
        }
      }
    )
  except botocore.exceptions.ClientError as e:
    handle_botocore_error(e)
  except Exception as e:
    print(e)
    raise InternalException()