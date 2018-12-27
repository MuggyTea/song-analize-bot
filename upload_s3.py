#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
import os, json, boto3

def sign_s3(file_name, file_type):
  S3_BUCKET = os.environ.get('song-analize-linebot')

  # file_name = request.args.get('file_name')
  # file_type = request.args.get('file_type')

  s3 = boto3.client('s3')

  presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )

  return json.dumps({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })