import os, base64, json, math
from flask import Flask, render_template, request, jsonify, send_from_directory

from aws.awsClient import AWSClient
from gps.location import Location

app = Flask(__name__, static_folder="build", template_folder="build")

awsClient = AWSClient()

location = Location()

## Face api
@app.route("/api/getCurrentFace", methods=['GET'])
def get_current_face():
    image = awsClient.getOwner()
    result = jsonify({'binary': base64.b64encode(image).decode()})
    return result

@app.route("/api/updateOwner", methods=['POST'])
def update_owner():
    request_data = request.files['image']
    awsClient.changeOwner(request_data)
    image = awsClient.getOwner()
    result = jsonify({'binary': base64.b64encode(image).decode()})
    return result

@app.route("/api/compare", methods=['POST'])
def compare():
    ## TODO: receive IMAGE from camera through api
    image = request.files['image']
    result = jsonify({'Success': awsClient.compare(image)})
    return result

@app.route("/api/getWeird", methods=['GET'])
def getWeird():
    images = awsClient.getAllWeirdPeople()
    result = jsonify({'all_data': images})
    return result


## GPS api
@app.route("/api/getLocation", methods=['GET'])
def getLocation():
    global location
    data = {
        "coordinates": location.data.get("gps", [121.543764, 25.019388]),
        "distance": location.data.get("distance", 0),
    }
    return jsonify(data)

@app.route("/api/updateLocation", methods=['POST'])
def updateLocation():
    global location
    try:
        data = json.loads(request.data)
        [MLonA, LatA] = location.data["gps"]
        [MLonB, LatB] = data["gps"]
        distance = location.data["distance"] + 6371004 * math.pi * math.acos(math.sin(LatA) * math.sin(LatB) + math.cos(LatA) * math.cos(LatB) * math.cos(MLonA-MLonB)) / 180
        location.data["gps"] = data["gps"]
        location.data["distance"] = distance

        result = jsonify({'Success': True})
        return result
    except Exception as e:
        result = jsonify({'Success': False, "errorMsg": str(e), "request": str(request.data)})
        return result

@app.route("/api/resetDistance", methods=["POST"])
def resetDistance():
    global location
    location.data["distance"] = 0
    return jsonify({'Success': True})


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, threaded=True)
    

# app.run(host="127.0.0.1", port=3000)
