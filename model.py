from flask_restx import Resource, Api, fields
from flask import Flask

app = Flask(__name__)
api = Api(app, version='0.0.3',
          title='CRW4Automation', default_label="below", default="Function")


general_payload = api.model('輸入', {
    'task_id': fields.String(required=True, default='task.id')
})

general_output = api.model('輸出', {
    'task_id': fields.String(required=True, default='task.id')
})

id_payload = api.model('ID輸入', {
    'id': fields.String(required=True, default='task.id')
})


count_output_data = api.model('模擬輸出', {
    "task_id": fields.String(required=True, default='task.id'),
    'status': fields.String(required=True, default='0')
})

