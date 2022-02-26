from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from netconf_comm.netconf_call import netconf_post, netconf_get
from util.request_validator import validate_request


app = Flask(__name__)
api = Api(app)


class AdminState(Resource):

    def get(self, interface_name):
        admin_state = netconf_get(interface_name)
        if admin_state is not None:
            return jsonify({'admin-state': admin_state})
        else:
            return jsonify({"info": "interface not configured"})


class Interface(Resource):

    def post(self):
        if request.is_json:
            data = request.get_json()
            if validate_request(data):
                if netconf_post(data):
                    return {"info": "request processed successfully"}, 201
                else:
                    return {"error": "request not processed to device"}, 204
            else:
                return {"error": "request not correct"}, 400
        return {"error": "request must be JSON"}, 415


api.add_resource(Interface, '/automation')
api.add_resource(AdminState, '/automation/<interface_name>')

if __name__ == '__main__':
    app.run(debug=True)
