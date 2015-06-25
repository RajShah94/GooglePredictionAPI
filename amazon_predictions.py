#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line sample for the Google Prediction API

Command-line application that trains on your input data. This sample does
the same thing as the Hello Prediction! example. You might want to run
the setup.sh script to load the sample data to Google Storage.

Usage:
  $ python amazon_predictions.py "bucket/object" "model_id" "project_id"

You can also get help on all the command-line flags the program understands
by running:

  $ python amazon_predictions.py --help

To get detailed log output run:

  $ python amazon_predictions.py --logging_level=DEBUG
"""




from __future__ import print_function

__author__ = ('jcgregorio@google.com (Joe Gregorio), '
              'marccohen@google.com (Marc Cohen)')


import argparse
import os
import pprint
import sys
import time
import urllib

from apiclient import discovery
from apiclient import sample_tools
from oauth2client import client


# Time to wait (in seconds) between successive checks of training status.
SLEEP_TIME = 10


# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('object_name',
    help='Full Google Storage path of csv data (ex bucket/object)')
argparser.add_argument('model_id',
    help='Model Id of your choosing to name trained model')
argparser.add_argument('project_id',
    help='Model Id of your choosing to name trained model')


def print_header(line):
  '''Format and print header block sized to length of line'''
  header_str = '='
  header_line = header_str * len(line)
  print('\n' + header_line)
  print(line)
  print(header_line)


############################################################################################
  # changes to the original file provided by Google.
  # This is a function to read the json file.
def readData(f):
  for l in urllib.urlopen(f):
    yield eval(l)
#############################################################################################
def main(argv):
  # If you previously ran this app with an earlier version of the API
  # or if you change the list of scopes below, revoke your app's permission
  # here: https://accounts.google.com/IssuedAuthSubTokens
  # Then re-run the app to re-authorize it.
  service, flags = sample_tools.init(
      argv, 'prediction', 'v1.6', __doc__, __file__, parents=[argparser],
      scope=(
          'https://www.googleapis.com/auth/prediction',
          'https://www.googleapis.com/auth/devstorage.read_only'))

  try:
    # Get access to the Prediction API.
    papi = service.trainedmodels()

    # List models.
    print_header('Fetching list of first ten models')
    result = papi.list(maxResults=10, project=flags.project_id).execute()
    print('List results:')
    pprint.pprint(result)

##################################################################################
# Uncomment this part only if you need to train a new model. I manually uploaded 
# my training file and inserted the model in Google prediction API as I found that 
# approach to be more convinient. While training multiple models, it might be a 
# better approach to use the below script rather than training the models manually.

    # Start training request on a data set.
    '''print_header('Submitting model training request')
    body = {'id': flags.model_id, 'storageDataLocation': flags.object_name}
    start = papi.insert(body=body, project=flags.project_id).execute()
    print('Training results:')
    pprint.pprint(start)

    # Wait for the training to complete.
    print_header('Waiting for training to complete')
    while True:
      status = papi.get(id=flags.model_id, project=flags.project_id).execute()
      state = status['trainingStatus']
      print('Training state: ' + state)
      if state == 'DONE':
        break
      elif state == 'RUNNING':
        time.sleep(SLEEP_TIME)
        continue
      else:
        raise Exception('Training Error: ' + state)

      # Job has completed.
      print('Training completed:')
      pprint.pprint(status)
      break

    '''
###################################################################################
    # Describe model.
    print_header('Fetching model description')
    result = papi.analyze(id=flags.model_id, project=flags.project_id).execute()
    print('Analyze results:')
    pprint.pprint(result)

####################################################################################

    # changes to the original code provided by Google.
    
    # Make some predictions using the newly trained model.

    print_header('Making some predictions') 

    # counter to print out the number of queries made
    i = 0

    # read the test file with each json object as an element in the list
    #
    test = list(readData("test.json"))

    # open the prediction file to write the actual rating and the predicted rating.
    # if modelling with categoires then change the file to be written to predictions_withCat.txt
    predictions = open("predictions.txt", 'w')
    
    # for each json object in the test file, send a query to the Google Prediction API 
    # and write the result and the actual rating to the prediction file.
    for l in test:

      
    # preparing the text for the query
      body = {'input': {'csvInstance': [l['itemID'],l['helpful'],l['text'],
      l['reviewerID'],l['categories'],l['unixReviewTime']]}}
      
    # making the query to the Google Prediction API
      result = papi.predict(
        body=body, id=flags.model_id, project=flags.project_id).execute()
      
    # writing the actual rating and the predicted rating to file
      predictions.write(str(l['rating']) + ' ' + str(result['outputLabel'])[10:] +  '\n')
      
    # print out the number of predictions made so far for every 1000 predictions made
      if i%1000 ==0:
        print('predictions made so far: ' + str(i))

    # increment the counter    
      i = i+1
        
    # close the prediction file
    predictions.close()

########################################################################################

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize.')

if __name__ == '__main__':
    main(sys.argv)
