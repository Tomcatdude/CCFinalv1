import json
import boto3
import botocore
import sys
import time
import os
from subprocess import call
import codecs

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
        local_file_name = '/tmp/bfstest.py'
        uploaded_file_name = KEY[::-1]
        uploaded_file_name = uploaded_file_name.split('/')[0]
        uploaded_file_name = uploaded_file_name[::-1]
        print(f'filename after full thing: {uploaded_file_name}')
        #mine KEY = f'private/us-east-1:8d6cf329-03e9-cb88-2d87-e615644e09e3/{uploaded_file_name}'
        #KEY = f'private/us-east-1:8d6cf329-03d3-ca78-1083-e83a96a75c95/{uploaded_file_name}'
        KEY = KEY.split('%3A')[0]+':'+KEY.split('%3A')[1]
        print(KEY)
    except Exception as e:
            print(f'error on getting names')
            print(e)
            errors.append('error on downloading file')

    try:
        
        KA_object = s3.Object(BUCKET_NAME, KEY) #get the object
        line_stream = codecs.getreader("utf-8")

        file_to_write_to = "/tmp/manager.py" #manager file to store the stuff
        if not os.path.isfile(file_to_write_to):#make the file if it does not exist yet
            with open(file_to_write_to, 'w') as fp:
                pass    


        #write the contents of uploaded file in S3 to manager
        raw = open(file_to_write_to, "r+")
        raw.truncate() #delete everything from it if it saved from last Lambda run
        for line in line_stream(KA_object.get()['Body']): #write files
            raw.write(line)
        raw.close()

        
        '''print("manager written to hopefully")
        f = open(file_to_write_to, "r")
        for line in f:
            print(f'line in manager: {line}')

        f.close()
        '''
        #import knight_attack
        sys.path.append('/tmp')
        try:
            sys.modules.pop('manager')
        except:
            print('module not imported yet')
        from manager import knight_attack


        passlist = []

        print('before test 1')
        abort = False
        while abort == False:
            #test 1
            start = time.time() #starting time
            if knight_attack(8, 1, 1, 2, 2) == 2:
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
            if knight_attack(8, 1, 1, 2, 3) == 1:
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
            if knight_attack(8, 0, 3, 4, 2) == 3:
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
            if knight_attack(8, 0, 3, 5, 2) == 4:
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
            if knight_attack(24, 4, 7, 19, 20) == 10:
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
            if knight_attack(100, 21, 10, 0, 0) == 11:
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
            if knight_attack(3, 0, 0, 1, 2) == 1:
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
            
            if knight_attack(3, 0, 0, 1, 1) is None:
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
        
        

    except Exception as e:

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
  