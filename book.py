from flask import request,Flask,jsonify
from flask_basicauth import BasicAuth

from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://mongo:mongo@cluster0.jhgevbw.mongodb.net/"
client = MongoClient(uri)

app = Flask(__name__) 

app.config['BASIC_AUTH_USERNAME']='username'
app.config['BASIC_AUTH_PASSWORD']='password'
basic_auth = BasicAuth(app)

db = client["students"]
collection = db["std_info"]
all_students = collection.find()

std_all = []
books=[
    {"id":1,"title":"Book 1","author":"Author 1"},
    {"id":2,"title":"Book 2","author":"Author 2"},
    {"id":3,"title":"Book 3","author":"Author 3"}
]
for std in all_students:
    std_all.append(std)
    
@app.route("/")
def Greet():
    return "<p>Welcome to Students Management API</p>"

@app.route("/students",methods=["GET"])
@basic_auth.required
def get_all_std():
    return jsonify({"books":std_all})

@app.route("/students/<int:std_id>",methods=["GET"])
@basic_auth.required
def get_std(std_id):
    for g in std_all:
        std_id = str(std_id)
        if  g["_id"] == std_id:
            std = g
            break
        else:
            std = None
    if std:
        return jsonify(std)
    else:
        return jsonify({"error":"Student not found"}),404

@app.route("/students",methods=["POST"])
@basic_auth.required
def create_std():
    data = request.get_json()
    new_book={
        "id":len(books)+1,
        "title":data["title"],
        "author":data["author"]
    }
    books.append(new_book)
    return jsonify(new_book),201

@app.route("/books/<int:book_id>",methods=["PUT"])
@basic_auth.required
def update_std(book_id):
    book = next((b for b in books if b["id"]==book_id),None)
    if book:
        data = request.get_json()
        book.update(data)
        return jsonify(book)
    else:
        return jsonify({"error":"Book not found"}),404




@app.route("/books/<int:book_id>",methods=["DELETE"])
@basic_auth.required
def delete_std(book_id):
    book = next((b for b in books if b["id"]==book_id),None)
    if book:
        books.remove(book)
        return jsonify({"message":"Book deleted successfully"}),200
    else:
        return jsonify({"error":"Book not found"}),404
    




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
