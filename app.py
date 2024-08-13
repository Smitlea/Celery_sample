
from celery.result import AsyncResult
from flask import request
from logger import logger
from flask_restx import Resource, Api, fields
from tasks import CRW4Auto, process_data, Celery_app, count
from model import app, api, general_payload, general_output, count_output_data, id_payload



@api.route('/count')
class CountResource(Resource):
    @api.marshal_with(count_output_data)
    def get(self):
        task = count.delay()
        return {'task_id': task.id, 'status': task}
    
@api.route('/add')
class Add(Resource):
    @api.marshal_with(general_output)
    def get(self):
        task = CRW4Auto.delay(0, 10)
        return {'task_id': task.id}
    
@api.route("/queue")
class Register(Resource):
    @api.expect(id_payload)
    @api.marshal_with(general_output)
    def post(self):
        data = api.payload
        id = data.get("id")
        task = process_data.delay(id)
        logger.info(f"Task ID: {task.id}")
        return {'task_id': task.id}
    

@api.route('/result')
class Result(Resource):
    @api.doc(params={'task_id': 'input'})
    def get(self):
        getTask = request.args.get('task_id')
        result = AsyncResult(getTask, app=Celery_app)

        if result.state == 'PENDING' and result.info is None:
            response = {
                'state': result.state,
                'current': result.current,
                'status': 'Task not found or pending...'
            }
        elif result.state != 'SUCCESS':
            response = {
                'state': result.state,
                'current': result.info.get('current', 0) ,
                'total': result.info.get('total', 1) ,
                'status': result.info.get('status', '')
            }
            if result.result:
                response['result'] = result.result
        else:
            response = {
                'state': result.state,
                'status': str(result.info) if result.info else 'Task failed'
            }
        
        return response

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
