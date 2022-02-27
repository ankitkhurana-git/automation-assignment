from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from netconf_comm.netconf_call import netconf_edit_config, netconf_get
from util.request_validator import validate_request

# import sqlite3 as sql


app = Flask(__name__)
api = Api(app)


class InterfaceState(Resource):
    """
    This is a class for implementing get operation of rest api.
    """

    def get(self, interface_name):
        """
        It takes interface name and returns admin and oper status of
        that interface received through NETCONF get operation.
        :param interface_name:
        :return: json output
        """
        try:
            admin_state, oper_status = netconf_get(interface_name)
            if admin_state and oper_status is not None:
                return jsonify({'admin-state': admin_state, "oper-status": oper_status})
            else:
                return jsonify({"info": "interface not configured"})
        except Exception as e:
            return {"error": str(e)}, 500


class InterfaceConfig(Resource):
    """
    This is a class for implementing post operation of rest api.
    """

    def post(self):
        """
        it posts interface details to the device and returns status code accordingly.
        :return: json output
        """
        try:
            if request.is_json:
                data = request.get_json()
                if validate_request(data):
                    if netconf_edit_config(data):
                        return {"info": "request processed successfully"}, 201
                    else:
                        return {"error": "request not processed to device"}, 500
                else:
                    return {"error": "request not correct"}, 400
            return {"error": "request must be JSON"}, 415
        except Exception as e:
            return {"error": str(e)}, 500


api.add_resource(InterfaceConfig, '/automation')
api.add_resource(InterfaceState, '/automation/<interface_name>')

if __name__ == '__main__':
    app.run(debug=True)
