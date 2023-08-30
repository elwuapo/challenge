import os
import requests


from sanic import Sanic
from sanic.response import json, text

app = Sanic('ms2')

timeout = 30

ms1     = os.environ.get('MS1', 'http://127.0.0.1:7000/')
session = requests.Session()

session.timeout = timeout
session.headers = {
    'Content-Type': 'application/json'
}

# Report
@app.get('api/v1/report/')
async def get_report(request):
    try:
        query_params = { 
            'id': request.args.get('id') 
        }

        response = session.get(ms1 + 'api/v1/report/', params=query_params)
        response.raise_for_status()
        response = response.json()

        return json(response, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)
    
@app.get('static/reports/<filename>')
async def get_report_file(request, filename):
    try:
        response = session.get(ms1 + 'static/reports/' + filename)
        response.raise_for_status()
        response = response.text

        return text(response, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)

@app.post('api/v1/report/')
async def post_report(request):
    try:
        response = session.post(ms1 + 'api/v1/report/', json=request.json)
        response.raise_for_status()
        response = response.json()

        return json(response, status=201)
    except Exception as e:
        return json({'error': str(e)}, status=500)

# Punch
@app.delete('api/v1/punch/')
async def delete_punches(request):
    try:
        response = session.delete(ms1 + 'api/v1/punch/')
        response.raise_for_status()

        return json({}, status=204)
    except Exception as e:
        return json({'error': str(e)}, status=500)
    
@app.post('api/v1/punch/')
async def post_punches(request):
    try:
        response = session.post(ms1 + 'api/v1/punch/')
        response.raise_for_status()
        response = response.json()

        return json(response, status=201)
    except Exception as e:
        return json({'error': str(e)}, status=500)
    
# Person
@app.delete('api/v1/person/')
async def delete_persons(request):
    try:
        response = session.delete(ms1 + 'api/v1/person/')
        response.raise_for_status()

        return json({}, status=204)
    except Exception as e:
        return json({'error': str(e)}, status=500)
    
@app.post('api/v1/person/')
async def post_persons(request):
    try:
        response = session.post(ms1 + 'api/v1/person/', json=request.json)
        response.raise_for_status()
        response = response.json()

        return json(response, status=201)
    except Exception as e:
        return json({'error': str(e)}, status=500)
    
@app.get('api/v1/person/')
async def get_persons(request):
    try:
        response = session.get(ms1 + 'api/v1/person/')
        response.raise_for_status()
        response = response.json()

        return json(response, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)
    

@app.get('api/v1/check/')
async def get_check(request):
    try:
        query_params = { 
            'id': request.args.get('id') 
        }

        response = session.get(ms1 + 'api/v1/check/', params=query_params)
        response.raise_for_status()
        response = response.json()

        return json(response, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)