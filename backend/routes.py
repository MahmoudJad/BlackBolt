from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))

# client = MongoClient(
#     f"mongodb://{app.config['MONGO_USERNAME']}:{app.config['MONGO_PASSWORD']}@localhost")
mongodb_service = os.environ.get('MONGODB_SERVICE')
mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')
mongodb_port = os.environ.get('MONGODB_PORT')

print(f'The value of MONGODB_SERVICE is: {mongodb_service}')

if mongodb_service == None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    # abort(500, 'Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

if mongodb_username and mongodb_password:
    url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}"
else:
    url = f"mongodb://{mongodb_service}"


print(f"connecting to url: {url}")

try:
    client = MongoClient(url)
except OperationFailure as e:
    app.logger.error(f"Authentication error: {str(e)}")

db = client.songs
db.songs.drop()
db.songs.insert_many(songs_list)

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# INSERT CODE HERE
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200 


@app.route("/count")
def count():
    count =  db.songs.count_documents({})
    return {"count": count}, 200 


@app.route("/songs")
def songs():
    all_songs = db.songs.find({})  # Fetch all songs
    return jsonify({"songs": parse_json(all_songs)}), 200


@app.route("/song/<int:id>")
def get_song_by_id(id):
    song = db.songs.find({"id": id})
    if not song:
        return jsonify({"song":f"{id}) not found"}), 404 
    return jsonify({"song":parse_json(song)}), 200 

@app.route("/song", methods=["POST"])
def create_song():
    #  first extract the song data from the request body and then append it to the data list.
    data = request.get_json()
    # If a song with the id already exists, send an HTTP code of 302 back to the user with a message of {"Message": "song with id {song['id']} already present"}.
    song = db.songs.find_one({"id": data["id"]})
    if song:
        return jsonify({"Message": f"song with id {data['id']} already present"}), 302
    else: 
        result = db.songs.insert_one(data)
        return jsonify({"inserted id": {"$oid": str(result.inserted_id)}}), 201    

@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    data = request.get_json()
    song = db.songs.find_one({"id": id})
    if not song:
        return jsonify({"Message": f"song with id {id} not found"}), 404
    song_data = {key: song[key] for key in data.keys() if key in song}
    if song_data == data:
        return jsonify({"message":"song found, but nothing updated"}), 200
    else:
        db.songs.update_one({"id": id}, {"$set": data})
        return jsonify({"updated id": id}), 200

@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    # Extract the song from the URL and delete it from the database
    song = db.songs.find_one({"id": id})
    if not song:
        return jsonify({"message": f"Song with id {id} not found"}), 404

    # Attempt to delete the song
    result = db.songs.delete_one({"id": id})

    if result.deleted_count == 0:
        return jsonify({"message": "Song found, but not deleted"}), 200
    else:
        return jsonify({"deleted_id": id}), 200    
  
