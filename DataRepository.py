from goodreads import client
from goodreads.user import GoodreadsUser
import os
import math
from pymongo import MongoClient
from bson.objectid import ObjectId

class DataRepository():
    client = MongoClient('localhost', 27017)
    db = client['Goodreads_Dataset']

    def __init__(self,user_start_id):
        self.user_start_id=user_start_id
    def get_users(self):
        return list(self.db['user'].find())
    def get_user_by_id(self,id):
        return self.db['user'].find_one({"_id" : id})
    def get_book_by_id(self,id):
        return self.db['books'].find_one({"_id" : id})

    def scrape_books(self):
        gc = client.GoodreadsClient(os.environ['goodreads_key'],os.environ['goodreads_secret'])
        gc.authenticate(os.environ["access_token"], os.environ["access_secret"])
        start_id=self.user_start_id

        open_list = []
        while(True):
            user_start = gc.user(start_id)
            user_friends = user_start.friends()
            for u_f in user_friends:
                open_list.append(u_f["id"])
                goodread_user=GoodreadsUser(u_f,gc)
                mongo_user=self.db['user'].find_one({'gid':u_f["id"]})
                if mongo_user is None and int(u_f['reviews_count'])>5:

                    mongo_user={"gid":u_f["id"],
                          "name":u_f["name"],
                          "reviews_count":u_f["reviews_count"],
                          "image_url":u_f["image_url"]
                    }
                    user_id=self.db['user'].insert_one(mongo_user).inserted_id
                    pages = math.floor(int(u_f['reviews_count']) / 20)+2
                    for i in range(1,pages):
                        add_reviews=True
                        try:
                            reviews=goodread_user.reviews(page=i)
                        except:
                            add_reviews=False
                        if add_reviews:
                            for review in reviews:
                                try:
                                    mongo_book=self.db['books'].find_one({'id': review['book']['id']["#text"]})
                                    if mongo_book is None:
                                        mongo_book=dict(review['book'])
                                        mongo_book['id']=mongo_book['id']["#text"]
                                        mongo_book['text_reviews_count'] = mongo_book['text_reviews_count']["#text"]
                                        mongo_book['work'] = mongo_book['work']["id"]
                                        mongo_book_id=self.db['books'].insert_one(mongo_book).inserted_id
                                        mongo_book["_id"]=mongo_book_id
                                    mongo_book_id=mongo_book["_id"]
                                    if int(review['rating'])>0:
                                        mongo_review={"book_id":mongo_book_id,"rating":int(review['rating'])}
                                        self.db['user'].update_one(
                                            {"_id":user_id},
                                            {
                                                "$push":{"reviews":mongo_review}
                                            })
                                except:
                                    pass
            start_id=open_list.pop(0)






