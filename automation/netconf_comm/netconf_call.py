from ncclient import manager
from util.constants import *
import xmltodict

conn = manager.connect(host='127.0.0.1', port=port, username=username, password=password,
                       hostkey_verify=host_verify)


def netconf_edit_config(data):
    interface_data = """
         <config>
             <interfaces xmlns="http://automation/interfaces">
                <interface>
                    <name>{0}</name>
                    <description>Interface</description>
                    <admin-state>{1}</admin-state>
                    <oper-status>{2}</oper-status>
                    <vlan>256</vlan>
                    <ip-address>{3}</ip-address>
                </interface>
            </interfaces>
         </config>
     """.format(data["interface-name"], "down" if data["shutdown"] == "yes" else "up",
                "down" if data["shutdown"] == "yes" else "up", data["ip-address"])
    reply = conn.edit_config(
        target="running", config=interface_data, default_operation="merge"
    )

    return reply.ok


def netconf_get(interface_name):
    interface_data = """   
             <interfaces xmlns="http://automation/interfaces">
                <interface>
                    <name>{}</name>
                </interface>
            </interfaces>
     """.format(interface_name)
    reply = conn.get(filter=("subtree", interface_data))
    data = xmltodict.parse(reply.xml)
    print(data)
    if data["rpc-reply"]["data"] is not None:
        return data["rpc-reply"]["data"]["interfaces"]["interface"]["admin-state"], \
               data["rpc-reply"]["data"]["interfaces"]["interface"]["oper-status"]
    else:
        return None, None
