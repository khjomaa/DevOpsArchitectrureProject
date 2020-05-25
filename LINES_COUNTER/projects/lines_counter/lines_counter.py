#!/usr/bin/env python

import os
import sys
import uuid
import boto3
import logging
import pymysql

__author__ = 'khalilj'
__creation_date__ = '05/16/2020'

logger = logging.getLogger(__name__)

# Get environment variables
try:
    logger_level = os.environ.get('LOG_LEVEL', 'INFO')
    db_host = os.environ['DB_HOST']
    db_username = os.environ['DB_USERNAME']
    db_password = os.environ['DB_PASSWORD']
    db_database = os.environ['DB_DATABASE']
    logger.setLevel(logger_level)
    logger.debug(f'DB_HOST: {db_host}, DB_USERNAME: {db_username}, DB_PASSWORD: {db_password}, DB_DATABASE: {db_database}')
except KeyError as e:
    logger.error(f"Please set the environment variable {e.args[0]}")
    sys.exit(1)

# Connection to MySQL
try:
    conn = pymysql.connect(db_host, user=db_username, passwd=db_password, db=db_database, connect_timeout=10)
except Exception as ex:
    logger.error(ex)
    logger.error("ERROR: Could not connect to MySql instance")
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    logger.debug(f"Event: {event}")
    bucket_name = str(event["Records"][0]["s3"]["bucket"]["name"])
    key_name = str(event["Records"][0]["s3"]["object"]["key"])
    logger.debug(f'bucket_name: {bucket_name}, key_name: {key_name}')
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=key_name)
    except Exception as e:
        logger.exception(str(e))
        sys.exit()

    logger.debug(f'OBJ: {obj}')
    obj_type = obj["ResponseMetadata"]["HTTPHeaders"]["content-type"]
    try:
        if obj_type != "application/x-directory":
            _date = obj["LastModified"]
            _amount_of_lines = int(len(obj['Body'].read().decode('utf-8').split("\n")))
            _object_path = f"s3://{bucket_name}/{key_name}"
            _id = str(uuid.uuid4())
            logger.debug(f'_id: {_id}, _date: {_date}, _amount_of_lines: {_amount_of_lines}, _object_path: {_object_path}, ')

            with conn.cursor() as cur:
                sql = "INSERT INTO `lines` (`id`, `object_path`, `date`, `amount_of_lines`) VALUES(%s, %s, %s, %s)"
                val = (_id, _object_path, _date, _amount_of_lines)
                logger.debug(f'SQL Query: {sql}, Values: {val}')
                cur.execute(sql, val)
                conn.commit()
                logger.info(f"{cur.rowcount} Record inserted successfully into lines table")
        else:
            logger.info(f'Folder {bucket_name}/{key_name} created')
    except Exception as e:
        logger.error('Unsupported file was uploaded and ignored')
        logger.error(f'ERROR: {e}')
