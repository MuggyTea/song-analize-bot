#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
import os, json
import settings
import boto3

def sign_s3(sorce_file, target):
 #
 # AWS Session
 #
 session = boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                               region_name=settings.AWS_REGION_NAME)
 s3 = session.resource('s3')

 bucket = s3.Bucket(settings.AWS_S3_BUCKET_NAME)
 bucket.upload_file(sorce_file, target)