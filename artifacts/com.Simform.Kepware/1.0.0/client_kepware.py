import sys
import logging
import time
import json
import awsiot.greengrasscoreipc.clientv2 as clientV2

import socket
import asyncio
from asyncua import Client

# Function to create an OPC UA client
async def create_opcua_client(kepware_endpoint, security_mode, policy, certificate_path, privatekey_path):
    # Create an OPC UA client
    client = Client(kepware_endpoint)

    # Set security settings if required
    if security_mode.lower() != "none":
        await client.set_security_string(f"{policy},{security_mode},{certificate_path},{privatekey_path}")
        client.application_uri = "urn:example.org:FreeOpcUa:python-opcua"
        client.secure_channel_timeout = 10000
        client.session_timeout = 10000

    return client

# Function to publish data to AWS IoT Core
async def publish_to_aws(ipc_client, topic, qos, payload):
    ipc_client.publish_to_iot_core(topic_name=topic, qos=qos, payload=payload)        

# Check internet connectivity
def check_internet_connection():
    remote_server = "www.google.com"
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((remote_server, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()
    
# Main function
async def starter():
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) < 9:
        print("Usage: python script.py <json_data> <kepware_name> <kepware_endpoint> <policy> <security_mode> <certificate_path> <privatekey_path> <topic>")
        sys.exit(1)
 
    # Parse command line arguments
    json_data, kepware_name, kepware_endpoint, policy, security_mode, certificate_path, privatekey_path, topic= sys.argv[1:9]    
    
    # Load JSON data
    recipe_data = json.loads(json_data)

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)

    # Flag to track server status
    disconnected_or_reinitializedor_or_unavailable = False

    while True:
        if check_internet_connection():
            try:            
                # Connect to the OPC UA server
                client = await create_opcua_client(kepware_endpoint, security_mode, policy, certificate_path, privatekey_path)
                # await client.connect()            
                        
                async with client:
                    # Retrieve information from the OPC UA server
                    root = client.nodes.root                
                    logging.debug("Children of root are: %s", await root.get_children())
                    objects = client.nodes.objects
                    logging.debug("child og objects are: ", await objects.get_children())

                    # Get OPC UA tags based on the specified devices and parameters
                    tags = [client.get_node(f"ns=2;s={kepware_name}.{device['device_name']}.{parameter}") for device in recipe_data for parameter in device['parameters']]

                    while True:
                        # Read tag values
                        tag_data = [round(await tag.read_value(), 3) for tag in tags]

                        # Prepare payload for AWS IoT Core
                        payload_dict = {}
                        count = 0
                        for device in recipe_data:
                            payload_dict['device'] = device['device_name']
                            for parameter in device['parameters']:
                                payload_dict[parameter] = tag_data[count]
                                count += 1

                            logging.debug(payload_dict)
                            payload = json.dumps(payload_dict)

                            # Publish payload to AWS IoT Core
                            try:
                                await publish_to_aws(clientV2.GreengrassCoreIPCClientV2(), topic, 0, payload)                    
                            except Exception as e:
                                logging.error(f"An error occurred: {e}")
                            payload_dict.clear()

                        # Wait for 5 seconds before reading tags again
                        await asyncio.sleep(5)

                        # Reset the flag if the server was previously disconnected or reinitialized
                        if disconnected_or_reinitializedor_or_unavailable:
                            disconnected_or_reinitializedor_or_unavailable = False

            except Exception as e:
                # Handle exceptions, log the error, and publish an error message to AWS IoT Core
                if not disconnected_or_reinitializedor_or_unavailable:
                    disconnected_or_reinitializedor_or_unavailable = True
                    logging.error("Server disconnected, reinitialized, or unavailable.")
                    logging.error(f"An error occurred: {e}")
                    if str(e) == "Connection is closed":
                        error_payload_dict = {"error": "Server disconnected, reinitialized, or unavailable"}
                        error_payload = json.dumps(error_payload_dict)
                    else:
                        error_payload_dict = {"error": str(e)}
                        error_payload = json.dumps(error_payload_dict)
                    try:
                        await publish_to_aws(clientV2.GreengrassCoreIPCClientV2(), topic, 0, error_payload)                    
                    except Exception as e:
                        logging.error(f"An error occurred: {e}")

                # Wait for 5 seconds before attempting to reconnect to the server
                await asyncio.sleep(5)
        else:
            # Wait for 30 seconds before attempting to reconnect to the internet
            await asyncio.sleep(30)
    
if __name__ == "__main__":    
    asyncio.run(starter())

