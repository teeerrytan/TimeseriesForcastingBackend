from QUANTAXIS.TSBoosting.TSBoosting import TS_Boosting_predict
from QAWebServer.basehandles import QABaseHandler
from QUANTAXIS.QAUtil import QASETTING
import pandas as pd
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas
import json
import time

class TestHandler(QABaseHandler):
    def set_default_headers(self):
        print("setting headers!!! analyze")
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","Content-Type, Authorization, Content-Length, X-Requested-With, x-token")
        self.set_header("Access-Control-Allow-Methods", "HEAD, GET, POST, PUT, PATCH, DELETE")
    def get(self):
        client = QASETTING.client
        database = client.mydatabase
        collection = database.uploaddata
        ref = collection.find()
        start = ref[0]['datetime']
        end = ref[ref.count()-1]['datetime']
        by = 'D'
        databaseid = 'mydatabase'
        collectionid = 'uploaddata'
        TS_Boosting_predict(start=start, end=end, by=by, databaseid=databaseid, collectionid=collectionid)


        collection_prediction = database.prediction
        ref_prediction = collection_prediction.find()
        prediction = pd.DataFrame(list(ref_prediction)).drop(columns = '_id')

        prediction_json = {
            'yAxisData': list(prediction['predict']),
            'xAxisData': list(map(lambda x : x.split(' ')[0],list(prediction['datetime']))),
            'label': 'Future',
            'colorPicked': '#519e19'
        }



        collection_past_predict = database.past_prediction
        ref_past_pred = collection_past_predict.find()
        past_pred = pd.DataFrame(list(ref_past_pred)).drop(columns = '_id')

        past_json = {
            'yAxisData': list(past_pred['y_t']),
            'xAxisData': list(map(lambda x: x.split(' ')[0], list(past_pred['datetime']))),
            'label': 'Past',
            'colorPicked': '#999997',
            'twoLines': True,
            'yAxisData2': list(past_pred['predict']),
            'label2': 'Past Prediction',
            'colorPicked2': '#999997',

        }
        messagebody = {
            'token': 'success',
            'past': past_json,
            'future': prediction_json
        }

        self.write(messagebody)
        #self.write(json.dumps(prediction_json))

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()
