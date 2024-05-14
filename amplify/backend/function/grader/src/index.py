import json
import boto3
import botocore
import sys
import time
import os
import importlib
from subprocess import call

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
    uploaded_file_name = ''

    
    errors = []
    try:
        print(f'the key: {KEY}')
        print(f'bucket name: {BUCKET_NAME}')
        
        uploaded_file_name = KEY[::-1]
        uploaded_file_name = uploaded_file_name.split('/')[0]
        uploaded_file_name = uploaded_file_name[::-1]
        print(f'filename after full thing: {uploaded_file_name}')
        KEY = f'private/us-east-1:8d6cf329-03e9-cb88-2d87-e615644e09e3/{uploaded_file_name}'
        local_file_name = f'/tmp/{uploaded_file_name}'
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
        knight_attack_module = importlib.import_module(uploaded_file_name[:-3])
        from bfstest import knight_attack
        print('made it past import')

        passlist = []

        print('before test 1')
        abort = False
        while abort == False:
            #test 1
            start = time.time() #starting time
            if knight_attack_module.knight_attack(8, 1, 1, 2, 2) == 2:
                full = time.time()-start #end time
                in_seconds = full%60
                if(in_seconds>2): #find if it took too long
                    passlist = ['long']
                    break
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([0,in_seconds])
                passlist

            #test 2
            start = time.time()
            if knight_attack_module.knight_attack(8, 1, 1, 2, 3) == 1:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([0,in_seconds])
                passlist
            
            #test 3
            start = time.time()
            if knight_attack_module.knight_attack(8, 0, 3, 4, 2) == 3:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([0,in_seconds])
                passlist
            
            #test 4
            start = time.time()
            if knight_attack_module.knight_attack(8, 0, 3, 5, 2) == 4:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([0,in_seconds])
                passlist

            #test 5
            start = time.time()
            if knight_attack_module.knight_attack(24, 4, 7, 19, 20) == 10:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([0,in_seconds])
                passlist

            #test 6
            start = time.time()
            if knight_attack_module.knight_attack(100, 21, 10, 0, 0) == 11:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([0,in_seconds])
                passlist

            #test 7
            start = time.time()
            if knight_attack_module.knight_attack(3, 0, 0, 1, 2) == 1:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([0,in_seconds])
                passlist


            #test 8
            start = time.time()
            
            if knight_attack_module.knight_attack(3, 0, 0, 1, 1) is None:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([1,in_seconds])
            else:
                full = time.time()-start
                in_seconds = full%60
                if(in_seconds>2):
                    passlist = ['long']
                    break
                passlist.append([0,in_seconds])
                passlist
            print('after test 8')
            abort = True

        results_str = ''
        for element in passlist:
            if element == 'long': #bad results, notify user
                results_str = 'long'
                break
            results_str += f'{element[0]}:{element[1]},'
        if results_str != 'long':
            results_str = results_str[:-1]#remove last comma
        

        print(f'results_str:{results_str}')

        table = boto3.resource('dynamodb').Table('Result-p5zv5jaxcngclm3guabixyiyre-main')
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

        #sys.path.pop()
        call('rm -rf /tmp/..?* /tmp/.[!.]* /tmp/*', shell=True)
        print('removed file')
        
        

    except Exception as e:
        #sys.path.pop()
        call('rm -rf /tmp/..?* /tmp/.[!.]* /tmp/*', shell=True)
        print('removed file from error')

        #bad results, notify the app
        results_str = 'long'

        table = boto3.resource('dynamodb').Table('Result-p5zv5jaxcngclm3guabixyiyre-main')
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
  