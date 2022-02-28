from flask import Flask
from flask_restful import Api
from rest_resources.resources import InterfaceConfig, InterfaceState, DbData

app = Flask(__name__)
api = Api(app)

api.add_resource(InterfaceConfig, '/automation')
api.add_resource(InterfaceState, '/automation/<interface_name>')
api.add_resource(DbData, '/automation/records')

if __name__ == '__main__':
    app.run(debug=True)
