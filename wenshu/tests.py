from django.test import TestCase
import pymongo
# Create your tests here.
if __name__ == '__main__':
    client = pymongo.MongoClient(host='localhost', port=27017)
    db_case = client.case
    judge_doc = db_case.judge_doc
    judge_curor = judge_doc.find()
    judge_doc_info = db_case.judge_doc_info
    
    result = judge_doc.find_one({"case_no":"（2019）陕08刑终251号"})
    print(result)
#{'_id': '822a1832-3edf-49d8-88{'_id': '822a1832-3edf-49d8-88c1-aa9400fe8063', 'case_no': '（2019）陕08刑终251号', 'case_type': '刑事案件', 'causes': ['故意伤害'], 'content': [{'text': '<p>（2c1-aa9400fe8063', 'case_no': '（2019）陕08刑终251号', 'case_type': '刑事案件', 'causes': ['故意伤害'], 'content': [{'text': '<p>（2