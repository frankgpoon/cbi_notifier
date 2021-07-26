class InternalException(Exception):
  pass

class ClientException(Exception):
  pass

def handle_botocore_error(err):
  error_code = err.response['Error']['Code']
  botocore_message = err.response['Error']['Message']
  print(f'{error_code}: {botocore_message}')
  raise InternalException()
