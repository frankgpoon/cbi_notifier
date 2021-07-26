from enum import Enum

class FlagColor(Enum):
  CLOSED = 'C'
  GREEN = 'G'
  YELLOW = 'Y'
  RED = 'R'


CBI_FLAG_COLOR_ENDPOINT = 'https://api.community-boating.org/api/flag' 

FLAG_COLOR_HISTORY_DDB_TABLE = 'FlagColorHistoryPrototype'
FLAG_COLOR_HISTORY_MOST_RECENT_INDEX = 'MostRecentIndex'

NOTIFIER_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:712071367312:cbiNotifierTopicPrototype'