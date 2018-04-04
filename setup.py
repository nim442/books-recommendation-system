import os
import pandas as pd
from scipy.sparse import csr_matrix
from bson.objectid import ObjectId

os.environ["goodreads_key"]='b3ULykyky8T07LAcKdlXQ'
os.environ["goodreads_secret"]='dUcc6K7WEos3Vyq2A2JkYX1iHMCuR8UK0cCFvZK1kc'

os.environ["access_token"]='kLeEvIkRdHHTBwQbB4U5mg'
os.environ["access_secret"]='EWBJSKBwlGJ59pLWgT8FRUCYzGyjSE1WYGgvhi4'
user_id="5ac14dd4819db688f999e243"
from DataRepository import DataRepository

dr = DataRepository(9616934)
def calculate_knn():
    try:
        df_matrix = pd.read_pickle("df_matrix")
    except:
        users = dr.get_users()
        flat_users = []
        for user in users:
            if 'reviews' in user:
                for review in user['reviews']:
                    flat_users.append({
                        "user_id": user["_id"],
                        "book_id": review["book_id"],
                        "rating": review["rating"]
                    })
        df = pd.DataFrame(flat_users)
        df_matrix = df.pivot('user_id', 'book_id', 'rating').fillna(0)
    index = df_matrix.index.get_loc(ObjectId(user_id))
    csr = csr_matrix(df_matrix.values)
    from sklearn.neighbors import NearestNeighbors
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(csr)
    distance, indices = model_knn.kneighbors(df_matrix.iloc[index, :].reshape(1, -1), n_neighbors=10)
    return df_matrix,distance,indices

def calculate_mean_books(df_matrix,distance,indices):
    user_books=[]
    closest_users=[]
    for idx,i in enumerate(indices[0]):
        if idx!=0:
            user=dr.get_user_by_id(df_matrix.index[i])
            user['distance']=distance[0][idx]
            closest_users.append(user)
            for review in user['reviews']:
                user_books.append({
                    "user_id": user["_id"],
                    "book_id": review["book_id"],
                    "rating": review["rating"]/distance[0][idx]
                })

    df=pd.DataFrame(user_books)
    df_matrix=df.pivot('book_id','user_id','rating').fillna(0)
    # csr=csr_matrix(df_matrix.values)
    # model_knn=NearestNeighbors(metric='cosine',algorithm='brute')
    # model_knn.fit(csr)
    # distance,indices=model_knn.kneighbors(csr,n_neighbors=10)
    # i-0
    book_means={}
    for i in range(0,df_matrix.shape[0]):
        book_means[str(df_matrix.index[i])]=df_matrix.iloc[i,0:10].mean()
    book_means=sorted(book_means.items(), key=lambda x: x[1],reverse=True)

    user=dr.get_user_by_id(ObjectId(user_id))
    exist_books={}
    for review in user['reviews']:
        exist_books[str(review["book_id"])]=1
        book=dr.get_book_by_id(review["book_id"])
        exist_books[book['title']]=1

    book_means=[b for b in book_means if b[0] not in exist_books]
    book_means=[(dr.get_book_by_id(ObjectId(b[0])),b[1]) for b in book_means]
    book_means=[b for b in book_means if b[0]['title'] not in exist_books]


    return book_means
    # with open("Output.txt", "w") as text_file:
    #     for b_m in book_means:
    #         text_file.write("%s"%b_m[0]['title'])
    #         text_file.write("\n")





