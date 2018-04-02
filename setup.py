import os
import pandas as pd
os.environ["goodreads_key"]='b3ULykyky8T07LAcKdlXQ'
os.environ["goodreads_secret"]='dUcc6K7WEos3Vyq2A2JkYX1iHMCuR8UK0cCFvZK1kc'

os.environ["access_token"]='kLeEvIkRdHHTBwQbB4U5mg'
os.environ["access_secret"]='EWBJSKBwlGJ59pLWgT8FRUCYzGyjSE1WYGgvhi4'

from DataRepository import DataRepository
dr=DataRepository(9616934)
users=dr.get_users()
flat_users=[]
for user in users:
    if 'reviews' in user:
        for review in user['reviews']:
            flat_users.append({
                "user_id":user["_id"],
                "book_id":review["book_id"],
                "rating":review["rating"]
            })
df=pd.DataFrame(flat_users)
df_matrix=df.pivot('book_id','user_id','rating').fillna(0)
i=0;