from flask import Flask
import uuid
import json
from Digit import Panel, Digit
from flask import request
import cPickle as pickle
import os
import traceback, sys

app = Flask(__name__)

sess = {}
DATA_DIR = './data'


@app.route("/observation/add", methods=['POST'])
def ovservation():
    '''
    Input:
    {
      'observation': {'color': 'green', 'numbers': ['1110111', '0010000'] },
      'sequence': 'b839e67c-d637-4afc-9241-63943c4fea83'
    }
    '''

    try:
        parsed = json.loads(request.data.replace("'", "\""))
        checkFormat(parsed)
    except Exception as e:
        return error('Invalid input data')

    try:
        if (len(sess) == 0):
            load()
        if parsed['sequence'] in sess:
            res = sess[parsed['sequence']].analyze(parsed['observation'])
            save(parsed['sequence'])
            return prepAns(json.dumps(res))
        else:
            return error('The sequence isn\'t found')
    except Exception, err:
        return error('Internal server error')


def save(sessId):
    pickle.dump(sess[sessId], open(DATA_DIR + '/' + sessId, "wb"))


def load():
    for file in os.listdir(DATA_DIR):
        sess[file] = pickle.load(open(DATA_DIR + '/' + file, "rb"))


def checkFormat(input):
    if ('observation' not in input):
        raise ValueError()

    if (input['observation']['color'] == 'red'):
        return

    if ('sequence' not in input or
                'color' not in input['observation'] or
                'numbers' not in input['observation']):
        raise ValueError()

    if (input['observation']['color'] != 'green'):
        raise ValueError()

    if (len(input['observation']['numbers']) != 2):
        raise ValueError()

    if (len([elem for elem in input['observation']['numbers'] if len(elem) != 7]) > 0):
        raise ValueError()


@app.route("/sequence/create", methods=['POST'])
def sequence():
    sessId = str(uuid.uuid4())
    sess[sessId] = Panel()
    save(sessId)
    print '> Sequence [', sessId, '] created.'
    seq_resp = {'status': 'ok', 'response': {'sequence': sessId}}
    return prepAns(json.dumps(seq_resp))


@app.route("/clear", methods=['GET'])
def clear():
    sess.clear()
    for the_file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e
    print '> All data cleared.'
    return prepAns(json.dumps({'status': 'ok', 'response': 'ok'}))


def error(msg):
    return prepAns(json.dumps({'status': 'error', 'msg': msg}))


def prepAns(json):
    return json.replace("\"", "'")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
