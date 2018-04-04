from flask import Flask
from setup import calculate_knn,calculate_mean_books
from bson.json_util import dumps
from DataRepository import DataRepository
from bson.objectid import ObjectId
from flask import g
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/get_knn")
def get_knn():
    dr=DataRepository()
    df_matrix, distance, indices = calculate_knn()

    book_means=calculate_mean_books(df_matrix, distance, indices)
    users={}
    for idx in indices[0]:
        users[str(idx)]=dr.get_user_by_id(ObjectId(df_matrix.index[idx]))

    response={"books":book_means,"distance":distance[0].tolist(),"indices":indices[0].tolist(),"users":users}
    return dumps(response)

@app.route("/update_neigbors")
def update_neighbors():
    pass
app.run('localhost', 5555,threaded=True)