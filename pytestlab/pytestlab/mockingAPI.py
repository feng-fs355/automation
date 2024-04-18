from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'This is a mocking page for rest api!'

@app.route('/json', methods=['POST', 'GET'])
def test_json():
    return '{"code": 1, "message": "Hello, World!" }'
    
# Run in HTTPS
ssl_context_ = ('Data/testssl.crt', 'Data/testssl.key')
app.run(host='127.0.0.1', port='8443', debug=True, ssl_context=ssl_context_)  
