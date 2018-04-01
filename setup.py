import os
os.environ["goodreads_key"]='b3ULykyky8T07LAcKdlXQ'
os.environ["goodreads_secret"]='dUcc6K7WEos3Vyq2A2JkYX1iHMCuR8UK0cCFvZK1kc'

os.environ["access_token"]='kLeEvIkRdHHTBwQbB4U5mg'
os.environ["access_secret"]='EWBJSKBwlGJ59pLWgT8FRUCYzGyjSE1WYGgvhi4'

from DataRepository import DataRepository
dr=DataRepository(17076701)
dr.scrape_books()