import os

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask_cors import CORS
from flask_cors import cross_origin

import twitter


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
twitter_api = twitter.Api(consumer_key=os.environ['CHANGEMYDP_CONSUMER_KEY'],
                          consumer_secret=os.environ['CHANGEMYDP_CONSUMER_SECRET'],
                          access_token_key=os.environ['CHANGEMYDP_ACCESS_TOKEN_KEY'],
                          access_token_secret=os.environ['CHANGEMYDP_ACCESS_TOKEN_SECRET'])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/change-dp', methods=['POST'])
@cross_origin()
def change_dp():
    base64_image = request.get_data(as_text=True)
    if base64_image == b'':
        return '{ "message": "Error. Cannot proceed with the operation." }'

    request_url = '%s/account/update_profile_image.json' % (twitter_api.base_url)
    resp = twitter_api._RequestUrl(request_url, 'POST', data={ 'image': base64_image })
    if resp.status_code in [200, 201, 202]:
        return '{ "message": "Successfully changed the profile picture." }'
    elif resp.status_code == 400:
        return '{ "message": "Something went wrong. Image data cannot be processed by Twitter. My bad. :(" }';
    elif resp.status_code == 422:
        return '{ "message": "Something went wrong. Picture is too big or cannot be resized. My bad. :( " }';


if __name__ == '__main__':
    app.run(debug=True)