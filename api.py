#######################
# API
#######################
from flask import *
from os import environ as env
import db
from functools import wraps

app = Flask(__name__)

app.secret_key = env.get("FLASK_SECRET")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Photos


@app.route("/api/photos/get", methods=['GET'])
@login_required
def getPhotosAPI():
    photos = db.get_photos()

    json = []
    for photo in photos:
        json.append({"id": photo[0], "title": photo[1], "description": photo[2], "location": photo[3],
                    "upload_date": photo[4], "image_url": photo[5], "user_id": photo[6]})

    return jsonify(json)


@app.route("/api/photos/get/<id>", methods=['GET'])
@login_required
def getPhotoAPI(id):
    photo = db.get_photos(id)
    json = {"id": photo[0], "title": photo[1], "description": photo[2], "location": photo[3],
            "upload_date": photo[4], "image_url": photo[5], "user_id": photo[6]}
    return jsonify(json)


@app.route("/api/photos/add", methods=['POST'])
@login_required
def addPhotoAPI():
    data = request.get_json()
    db.add_photo(data['id'], data['title'], data['description'], data['location'],
                 data['upload_date'], data['image_url'], data['user_id'])
    return jsonify({"success": True})


@app.route("/api/photos/delete/<id>", methods=['DELETE'])
@login_required
def deletePhotoAPI(id):
    db.delete_photo(id)
    return jsonify({"success": True})


@app.route("/api/photos/edit/<id>", methods=['PUT'])
@login_required
def editPhotoAPI(id):
    data = request.get_json()
    db.edit_photo(id, data['title'], data['description'], data['location'],
                  data['upload_date'], data['image_url'], data['user_id'])
    return jsonify({"success": True})

# Users


@app.route("/api/users/get_all", methods=['GET'])
@login_required
def getAllUsersAPI():
    users = db.get_all_users()
    json = []
    print(users)
    for user in users:
        json.append({"id": user[0], "username": user[1], "email": user[2],
                     "profile_pic": user[3], "saved_photos": user[4]})
    return jsonify(json)


@app.route("/api/users/get/<id>", methods=['GET'])
@login_required
def getUserAPI(id):
    user = db.get_user_by_id(id)
    json = {"id": user[0], "username": user[1], "email": user[2],
            "profile_pic": user[3], "saved_photos": user[4]}
    return jsonify(json)


@app.route("/api/users/get_by_username/<username>", methods=['GET'])
@login_required
def getUserByUsernameAPI(username):
    user = db.get_user_by_name(username)
    json = {"id": user[0], "username": user[1], "email": user[2],
            "profile_pic": user[3], "saved_photos": user[4]}
    return jsonify(json)


@app.route("/api/users/create", methods=['POST'])
@login_required
def createUserAPI():
    data = request.get_json()
    
    db.create_user(data['username'], data['email'], data['profile_pic'])
    return jsonify({"success": True})


@app.route("/api/users/delete/<id>", methods=['DELETE'])
@login_required
def deleteUserAPI(id):
    db.delete_user(id)
    return jsonify({"success": True})


@app.route("/api/users/edit/<id>", methods=['PUT'])
@login_required
def editUserAPI(id):
    data = request.get_json()
    db.edit_user(id, data['username'], data['email'], data['profile_pic'])
    return jsonify({"success": True})

# Saved Photos


@app.route("/api/users/add_save_photo/<user_id>/<photo_id>", methods=['PUT'])
@login_required
def addSavePhotoAPI(user_id, photo_id):
    db.add_saved_photos(user_id, photo_id)
    return jsonify({"success": True})


@app.route("/api/users/remove_saved_photo/<user_id>/<photo_id>", methods=['DELETE'])
@login_required
def removeSavedPhotoAPI(user_id, photo_id):
    db.remove_saved_photos(user_id, photo_id)
    return jsonify({"success": True})


@app.route("/api/users/get_saved_photos/<user_id>", methods=['GET'])
@login_required
def getSavedPhotosAPI(user_id):
    photos = db.get_saved_photos(user_id)
    json = []
    for photo in photos:
        json.append({"id": photo[0], "title": photo[1], "description": photo[2], "location": photo[3],
                    "upload_date": photo[4], "image_url": photo[5], "user_id": photo[6]})
    return jsonify(json)


@app.route("/api/users/get_saved_photos/<user_id>/<photo_id>", methods=['GET'])
@login_required
def getSavedPhotoAPI(user_id, photo_id):
    photo = db.get_saved_photo(user_id, photo_id)
    json = {"id": photo[0], "title": photo[1], "description": photo[2], "location": photo[3],
            "upload_date": photo[4], "image_url": photo[5], "user_id": photo[6]}
    return jsonify(json)

# Comments


@app.route("/api/comments/create", methods=['POST'])
@login_required
def createCommentAPI():
    data = request.get_json()
    db.create_comment(data['user_id'], data['photo_id'], data['comment'])
    return jsonify({"success": True})


@app.route("/api/comments/get/<photo_id>", methods=['GET'])
@login_required
def getCommentsbyPhotoIdAPI(photo_id):
    comments = db.get_comments_by_photo_id(photo_id)
    json = []
    for comment in comments:
        json.append({"id": comment[0], "comment": comment[1],
                    "user_id": comment[2], "photo_id": comment[3], })
    return jsonify(json)


@app.route("/api/comments/get/<user_id>", methods=['GET'])
@login_required
def getCommentsbyUserIdAPI(user_id):
    comments = db.get_comments_by_user_id(user_id)
    json = []
    for comment in comments:
        json.append({"id": comment[0], "comment": comment[1],
                    "user_id": comment[2], "photo_id": comment[3], })
    return jsonify(json)


@app.route("/api/comments/delete/<id>", methods=['DELETE'])
@login_required
def deleteCommentAPI(id):
    db.delete_comment(id)
    return jsonify({"success": True})


@app.route("/api/comments/edit/<id>", methods=['PUT'])
@login_required
def editCommentAPI(id):
    data = request.get_json()
    db.edit_comment(id, data['comment'])
    return jsonify({"success": True})

# Likes


@app.route("/api/likes/create", methods=['POST'])
@login_required
def createLikeAPI():
    data = request.get_json()
    db.add_like(data['user_id'], data['photo_id'])
    return jsonify({"success": True})


@app.route("/api/likes/get/<photo_id>", methods=['GET'])
@login_required
def getLikesbyPhotoIdAPI(photo_id):
    likes = db.get_likes_by_photo_id(photo_id)
    json = []
    for like in likes:
        json.append({"id": like[0], "user_id": like[1], "photo_id": like[2]})
    return jsonify(json)


@app.route("/api/likes/get/<user_id>", methods=['GET'])
@login_required
def getLikesbyUserIdAPI(user_id):
    likes = db.get_likes_by_user_id(user_id)
    json = []
    for like in likes:
        json.append({"id": like[0], "user_id": like[1], "photo_id": like[2]})
    return jsonify(json)


@app.route("/api/likes/delete/<id>", methods=['DELETE'])
@login_required
def deleteLikeAPI(id):
    db.remove_like(id)
    return jsonify({"success": True})