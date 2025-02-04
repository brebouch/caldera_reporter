import json
from pymongo import MongoClient


class MongoDB:
    def __init__(self, db_name, collection_name, host='localhost', port=27017):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, json_data):
        # Convert JSON string to a Python dictionary
        data = json.loads(json_data)
        result = self.collection.insert_one(data)
        return json.dumps({'inserted_id': str(result.inserted_id)})

    def read_documents(self, json_query=None):
        if json_query is None:
            query = {}
        else:
            query = json.loads(json_query)
        documents = list(self.collection.find(query))
        # Convert ObjectId to string and return JSON string
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return json.dumps(documents)

    def update_document(self, json_query, json_update_data):
        query = json.loads(json_query)
        update_data = json.loads(json_update_data)
        result = self.collection.update_one(query, {'$set': update_data})
        return json.dumps({'modified_count': result.modified_count})

    def delete_document(self, json_query):
        query = json.loads(json_query)
        result = self.collection.delete_one(query)
        return json.dumps({'deleted_count': result.deleted_count})

    def close_connection(self):
        self.client.close()

# Example usage:
# db_crud = MongoDBCrud('my_database', 'my_collection')
# inserted_id_json = db_crud.create_document(json.dumps({'name': 'John Doe', 'age': 30}))
# print('Inserted Document ID JSON:', inserted_id_json)
# documents_json = db_crud.read_documents(json.dumps({'name': 'John Doe'}))
# print('Documents JSON:', documents_json)
# updated_count_json = db_crud.update_document(json.dumps({'name': 'John Doe'}), json.dumps({'age': 31}))
# print('Updated Document Count JSON:', updated_count_json)
# deleted_count_json = db_crud.delete_document(json.dumps({'name': 'John Doe'}))
# print('Deleted Document Count JSON:', deleted_count_json)
# db_crud.close_connection()