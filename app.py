from flask import Flask, request
from flask_restx import Api, Resource, reqparse, swagger,fields, marshal_with, marshal
from datetime import datetime
import re
import json

app = Flask(__name__)
api = Api(app,
          title="CanvasPlusPlus",
          description="API to improve Canvas Calendar to Google Calendar functionality")

in_payload_args = reqparse.RequestParser()
in_payload_args.add_argument("postData", help="postData not received.", required=True)
# in_payload_args.add_argument("blacklistData", type=str, help="Blacklist required!", required=True)
# in_payload_args.add_argument("separateData", type=bool, help="Separation data required!", required=True)
# in_payload_args.add_argument("excludeEventsData", type=bool, help="Exclusion data link required!", required=True)

link_as_string = []
generated_cals = {"links": link_as_string}


class ProcessData(Resource):
    #@api.doc(params={'inputJSON'})
    def post(self):
        args = in_payload_args.parse_args()
        #userdict = args['postData']  # dictionary that contains data sent from frontend
        return generated_cals  # provide a dictionary with one key-value pair containing a list of calendar links


api.add_resource(ProcessData, "/api/PostCal")


@app.route("/hey")
def home():
    return "Hello, Here!"


if __name__ == "__main__":
    app.run(debug=True)
