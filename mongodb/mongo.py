import pymongo
# import certifi

client = pymongo.MongoClient("mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority")

post = client['core_data']['post']

"""
CRUD 요청
"""
# 추가하는 코드 create
# post.insert_one({'title': '테스트용 현호', 'content': 'ㅁㄴㅇㄹ'})

# 삭제 delete
# post.delete_one({'title': '테스트용 현호'})

# 업데이트 update
# post.update_one({'title': '테스트용 현호'}, {'$set': {'content' : '밥'} } )

# 읽기 read
data = post.find()

for data in data:
    print(data)

