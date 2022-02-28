from ncclient import manager
from util.constants import *
import xmltodict
from automation_db.db_operations import insert_device_record

conn = manager.connect(host='10.0.2.15', port=port, username=username, password=password,
                       hostkey_verify=host_verify)


def netconf_edit_config(data):
    """
    This function takes input post data and pushes it to device using NETCONF edit-config call.
    :param data:
    :return: boolean
    """
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

    insert_device_record(data["interface-name"], "post", "edit-config", str(reply.ok))
    return reply.ok


def netconf_get(interface_name):
    """
    This function checks for the interface admin and oper status using NETCONF get call.
    :param interface_name:
    :return: admin state, oper status
    """
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
        admin_state = data["rpc-reply"]["data"]["interfaces"]["interface"]["admin-state"]
        oper_status = data["rpc-reply"]["data"]["interfaces"]["interface"]["oper-status"]

        insert_device_record(interface_name, "get", "get", "admin-status: {}".format(admin_state) )

        return admin_state, oper_status

    else:
        insert_device_record(interface_name, "get", "get", "Interface not configured")
        return None, None
