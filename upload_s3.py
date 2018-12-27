#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
import os, json, boto3
import settings

def sign_s3(file_name, file_type):
 #
 # AWS Session
 #
 session = boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                               region_name=settings.AWS_REGION_NAME)
 s3 = session.resource('s3')
 bucket = s3.Bucket(settings.AWS_S3_BUCKET_NAME)

 obj = bucket.Object(file_name)
 response = obj.put(
 Body=file_name,
 ContentEncoding='utf-8',
 ContentType=file_type
 )

