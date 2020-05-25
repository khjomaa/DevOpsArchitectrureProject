#!/usr/bin/env python

import os
import sys
import boto3
import shutil
import errno
import logging
import pymysql
import requests
from requests.exceptions import Timeout, ConnectionError
from datetime import datetime, timedelta
from dateutil.tz import tzutc

__author__ = 'khalilj'
__creation_date__ = '05/16/2020'

# Logger
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

local_folder = 's3_bucket'
all_objects = {}
objects_for_db = {}


def connect_to_db():
    try:
        conn = pymysql.connect(db_host, user=db_username, passwd=db_password, db=db_database, connect_timeout=10)
        logger.info("Connected to RDS MySQL")
        return conn
    except Exception as ex:
        logger.exception(ex)
        logger.exception("ERROR: Could not connect to MySql instance")
        sys.exit()


def mkdir_p(path):
    """
    Create folders same as S3 bucket structure
    :param path: path of folder
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_s3_path_filename(key):
    """
    Get file path on S3 bucket
    :param key: file name
    :returns file path on the bucket and file name
    """
    key = str(key)
    return key.replace(key.split('/')[-1], ""), key.split('/')[-1]


def download_s3_bucket(s3_bucket, bucket_name):
    """
    Download all files added to the bucket in the last 24 hours and file size <= 3KB.
    The files will be saved in folder with the same files & folders structure in S3 Bucket
    Also all files will be save to a dict which will be used later in count_words function
    :param bucket_name: S3 bucket name
    :param s3_bucket: S3 bucket object
    """
    objects_key = 1
    for obj in s3_bucket.objects.all():
        if obj.last_modified > datetime.now(tzutc()) - timedelta(hours=24):
            s3_obj = boto3.client('s3').get_object(Bucket=bucket_name, Key=obj.key)
            logger.debug(f'S3 Object: {s3_obj}')
            content_length = int(s3_obj['ResponseMetadata']['HTTPHeaders']['content-length'])
            logger.info(f'Content-Length: {content_length}')
            if content_length <= 3000:
                s3_path, s3_filename = get_s3_path_filename(obj.key)
                logger.debug(f'Downloading s3://{s3_path}{s3_filename}')
                local_folder_path = os.path.join(*[os.curdir, local_folder, s3_path])
                local_fullpath = os.path.join(*[local_folder_path, s3_filename])
                mkdir_p(local_folder_path)
                _date = str(s3_obj["LastModified"])
                if not os.path.isdir(local_fullpath):
                    all_objects[objects_key] = {
                        'object_path': f's3://{bucket_name}/{obj.key}',
                        'upload_date': _date
                    }
                    objects_key += 1
                    s3_bucket.download_file(obj.key, local_fullpath)
                else:
                    logger.debug(f'{local_fullpath} is a directory')

    logger.debug(all_objects)


def count_words():
    """
    Loop over all downloaded files recursively and send content to OpenFaaS words-counter function.
    Folders and non readable files (i.e: images) will be ignored

    :returns list of files to save in table words
    """
    headers = {'Content-Type': 'text/plain'}
    objects_for_db_key = 1
    for k, v in all_objects.items():
        local_file_path = v['object_path'].replace('s3://khalilj-files-bucket', local_folder)
        if os.path.isfile(local_file_path):
            try:
                with open(local_file_path, 'r') as f:
                    payload = f.read()
                    res = requests.get(words_counter_url, headers=headers, data=payload, timeout=10)
                    res.encoding = 'utf-8'
                    objects_for_db[objects_for_db_key] = {
                        'object_path': v['object_path'],
                        'upload_date': v['upload_date'],
                        'amount_of_words': int(res.text)
                    }
                    objects_for_db_key += 1
            except (Timeout, ConnectionError) as e:
                logger.error(f'Could not connect to OpenFaaS function {words_counter_url}')
                logger.error(e)
                sys.exit()
            except Exception as e:
                logger.debug(f'Failed to read file {local_file_path}')
                logger.debug(f'ERROR: {e}')

        else:
            logger.debug(f'{local_file_path} is not a file')

    logger.debug(objects_for_db)


def save_to_db():
    try:
        conn = connect_to_db()
        for k, v in objects_for_db.items():
            _object_path = v['object_path']
            _date = v['upload_date']
            _amount_of_words = v['amount_of_words']
            with conn.cursor() as cur:
                sql = "INSERT INTO `words` (`object_path`, `date`, `amount_of_words`) VALUES(%s, %s, %s)"
                val = (_object_path, _date, _amount_of_words)
                cur.execute(sql, val)
                conn.commit()
                logger.info(f"{cur.rowcount} Record inserted successfully into words table")
    except Exception as e:
        logger.debug('Something went wrong')
        logger.exception(e)


def main(bucket):
    # Download files added to S3 Bucket int he last 24 hours
    # Return if no files were added in the last 24 hours
    logger.info(f'Downloading files added in the last 24 hours to S3 bucket [ {aws_bucket} ]')
    download_s3_bucket(s3_bucket=bucket, bucket_name=aws_bucket)
    if os.path.exists(local_folder):
        logger.info('Finished downloading files added in the past 24 hours ')
    else:
        logger.warning(f'No files were added in the last 24 hours')
        return

    # Send files content words_counter function in OpenFaaS
    # Return if no data to save to table words in the DB
    count_words()
    if not objects_for_db:
        logger.warning('No files to save to words table')
        return

    # Save to words table number of words on each file
    logger.info('Saving files info to words tables in the DB')
    save_to_db()

    shutil.rmtree(local_folder)


if __name__ == '__main__':
    logger.setLevel('INFO')

    try:
        logger_level = os.environ.get('LOG_LEVEL', 'INFO')
        db_host = os.environ['DB_HOST']
        db_username = os.environ['DB_USERNAME']
        db_password = os.environ['DB_PASSWORD']
        db_database = os.environ['DB_DATABASE']
        aws_bucket = os.environ['AWS_BUCKET']
        aws_region = os.environ['AWS_REGION']
        words_counter_url = os.environ['WORDS_COUNTER_URL']
    except KeyError as e:
        logger.error(f"Please set the environment variable {e.args[0]}")
        sys.exit(1)

    logger.setLevel(logger_level)

    s3 = boto3.resource('s3', region_name=aws_region)
    main(bucket=s3.Bucket(aws_bucket))
