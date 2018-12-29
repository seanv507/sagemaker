# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os
import subprocess
import json
import pickle
import io
import sys
import signal
import traceback

import flask

import pandas as pd

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')
output_path = os.path.join(prefix, 'output')
model_file = os.path.join(model_path, 'model.bin')
data_file = os.path.join(output_path, 'data.vw')
predictions_file = os.path.join(output_path, 'predictions.txt')

# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = os.path.exists(os.path.join(model_path, 'model.bin'))  # You can insert a health check here
    print('model exists')
    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data.
    """
    data = None
    
    if flask.request.content_type == 'application/x-vowpalwabbit':
        data = flask.request.data.decode('utf-8')
        with open(data_file, 'w') as d:
            d.write(data)
        vw_command = ('vw -i {} --data {} --testonly --link logistic --loss_function logistic '
                      '--predictions {}'
                      ).format(model_file, data_file,
                               predictions_file)
        stderr = subprocess.check_output(vw_command, shell=True, 
                                         timeout=60 * 20,
                                         stderr=subprocess.STDOUT).decode('utf-8')
        # tried stdin pipe but gunicorn complained no file no ...?
        print(stderr)
    else:
        return flask.Response(response='This predictor only supports vowpalwabbit data', status=415, mimetype='text/plain')
    
    # get the prediction
    with open(predictions_file) as f:
        predictions = f.read()
    
    return flask.Response(response=predictions, status=200, mimetype='text/csv')
