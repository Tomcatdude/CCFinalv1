import json
import boto3
import botocore
import sys
import time

def handler(event, context):
    print('received event:')
    print(event)

    records = [x for x in event.get('Records', []) if x.get('eventName') == 'ObjectCreated:Put']
    sorted_events = sorted(records, key=lambda e: e.get('eventTime'))
    latest_event = sorted_events[-1] if sorted_events else {}
    info = latest_event.get('s3', {})

    KEY = info.get('object', {}).get('key')
    BUCKET_NAME = info.get('bucket', {}).get('name')

    s3 = boto3.resource('s3')

    
    errors = []
    try:
        print(f'the key: {KEY}')
        print(f'bucket name: {BUCKET_NAME}')
        local_file_name = '/tmp/bfstest.py'
        KEY = 'private/us-east-1:8d6cf329-0336-cc7d-cc77-8309b09c4fb5/bfstest.py'
        print(f'manual input key: {KEY}')
        s3.Bucket(BUCKET_NAME).download_file(KEY, local_file_name)
        print('downloading file worked!')
    except Exception as e:
            print(f'error on downloading file')
            print(e)
            errors.append('error on downloading file')

    try:
        print('right on top of import')
        sys.path.append('/tmp')
        print(f'path: {sys.path}')
        from bfstest import knight_attack
        print('made it past import')

        passlist = []

        print('before test 1')
        abort = False
        while abort == False:
            #test 1
            start = time.time()
            if knight_attack(8, 1, 1, 2, 2) == 2:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([0,in_seconds])
                passlist

            #test 2
            start = time.time()
            if knight_attack(8, 1, 1, 2, 3) == 1:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([0,in_seconds])
                passlist
            
            #test 3
            start = time.time()
            if knight_attack(8, 0, 3, 4, 2) == 3:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([0,in_seconds])
                passlist
            
            #test 4
            start = time.time()
            if knight_attack(8, 0, 3, 5, 2) == 4:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([0,in_seconds])
                passlist

            #test 5
            start = time.time()
            if knight_attack(24, 4, 7, 19, 20) == 10:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([0,in_seconds])
                passlist

            #test 6
            start = time.time()
            if knight_attack(100, 21, 10, 0, 0) == 11:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([0,in_seconds])
                passlist

            #test 7
            start = time.time()
            if knight_attack(3, 0, 0, 1, 2) == 1:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([0,in_seconds])
                passlist


            #test 8
            start = time.time()
            if knight_attack(3, 0, 0, 1, 1) is None:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                passlist.append([0,in_seconds])
                passlist
            print('after test 8')
            abort = True

        results_str = ''
        for element in passlist:
            if element == 'long':
                results_str = 'long'
                break
            results_str += f'{element[0]}:{element[1]},'
        results_str = results_str[:-1]#remove last comma
        

        print(f'results_str:{results_str}')

        table = boto3.resource('dynamodb').Table('Result-urfzxobpc5bozecdt6sawncklq-dev')
        table.update_item(
            Key={'id': 'root',},
            UpdateExpression='SET #R = :r',
            ExpressionAttributeValues={
                ':r': results_str,
            },
            ExpressionAttributeNames={
                '#R': 'result',
            }
        )
        
        

    except Exception as e:
        print('error on this side')
        print(e)
        errors.append('failed on import of the thing')
    
    return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps(errors)
    }
  