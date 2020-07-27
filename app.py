import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from t import LandDetails

app = Flask(__name__)
cors = CORS(app)

@app.route('/hello/', methods=['GET', 'POST'])
@cross_origin()
def welcome():
    return "Hello World!"

@app.route('/landRecordDetails', methods=['POST'])
@cross_origin()
def landrecord():
    record = json.loads(request.data)
    ld = LandDetails()
    ld.getlandrecordinfo(record["landrec"],record["district"],record["taluka"],record["village"],record["surveyno"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1405,debug=True)