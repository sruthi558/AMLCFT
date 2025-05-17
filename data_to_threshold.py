from pymongo import MongoClient
import json

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['testBank']

with open('Query_Threshold.json', 'r') as file:
    data = json.load(file)

for alert in data.get('alerts', []):
    if isinstance(alert, dict):
        code_prefix = alert.get('code', '')[:2].upper()
        if code_prefix:
            collection_name = f'{code_prefix}'
            collection = db[collection_name]
            print(alert['code'])
            
            existing_document = collection.find_one({'code': alert['code']})
            
            if existing_document:
                result = collection.update_one(
                    {'code': alert['code']},
                    {'$set': {'Current_values': alert['Current_values'],'Alert_title':alert['Alert_title']}}
                )
                
                if result.modified_count > 0:
                    print(f"Document updated with code: {alert['code']}")
             
            else:
                result = collection.insert_one({'code': alert['code'], 'Current_values': alert['Current_values'],'Alert_title':alert['Alert_title']})
                
                if result.inserted_id:
                    print(f"Document inserted with _id: {result.inserted_id}")
                else:
                    print("Failed to insert document")
