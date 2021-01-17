from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from datetime import datetime
import re

app = Flask(__name__)
api = Api(app)

in_payload_args = reqparse.RequestParser()
in_payload_args.add_argument("inputLinkData", type=str, help="Canvas calendar link required!", required=True)
in_payload_args.add_argument("blacklistData", type=str, help="Blacklist required!", required=True)
in_payload_args.add_argument("seperateData", type=bool, help="Separation data required!", required=True)
in_payload_args.add_argument("excludeEventsData", type=bool, help="Exclusion data link required!", required=True)


class ProcessData(Resource):
    def post(self):
        args = in_payload_args.parse_args()
        return {"calLink": args["inputLinkData"]}


api.add_resource(ProcessData, "/api/PostCal")

@app.route("/")
def home():
    return "Hello, Here!"


if __name__ == "__main__":
    app.run(debug=True)