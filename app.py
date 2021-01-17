from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, marshal
from datetime import datetime
import re
import json

app = Flask(__name__)
api = Api(app)

in_payload_args = reqparse.RequestParser()
in_payload_args.add_argument("postData", type=dict, help="postData not received.", required=True)
# in_payload_args.add_argument("blacklistData", type=str, help="Blacklist required!", required=True)
# in_payload_args.add_argument("separateData", type=bool, help="Separation data required!", required=True)
# in_payload_args.add_argument("excludeEventsData", type=bool, help="Exclusion data link required!", required=True)

link_as_string = []
generated_cals = {"links": link_as_string}


class ProcessData(Resource):
    def post(self):
        args = in_payload_args.parse_args()
        userdict = args['postData']  # dictionary that contains data sent from frontend
        return generated_cals  # provide a dictionary with one key-value pair containing a list of calendar links


api.add_resource(ProcessData, "/api/PostCal")


@app.route("/")
def home():
    return "Hello, Here!"


if __name__ == "__main__":
    app.run(debug=True)
