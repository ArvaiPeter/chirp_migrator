from chirpstack_api import api
import grpc

old_server = "192.168.0.99:8080"
new_server = "192.168.0.98:8080"

old_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6ImQ2ZjdkYzQ2LTQ1YmQtNGE2Yi1iZWQ2LTAxMDJmMjQ3MzExYSIsInR5cCI6ImtleSJ9.-DRzhxQpOSz6e3D9NrC3ZePQ5hYkITJsu-AYYpjBksc"
new_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6Ijc2N2NlNGQ5LTZmYzctNDBhYi1hNmY1LTdjZDdhNjU5YzdiZiIsInR5cCI6ImtleSJ9.tWx8il54BpZC-uf5OPLCdL_ewvmnPX3LdS0z8cUHQaQ"

old_channel = grpc.insecure_channel(old_server)
new_channel = grpc.insecure_channel(new_server)

old_client = api.DeviceServiceStub(old_channel)
new_client = api.DeviceServiceStub(new_channel)

old_auth_token = [("authorization", "Bearer %s" % old_api_key)]
new_auth_token = [("authorization", "Bearer %s" % new_api_key)]


old_devices_request = dev.ListDevicesRequest(limit=0,
                             offset=0, 
                             search="", 
                             application_id="aafbbc5d-acda-4019-9eb5-5a5056e626a2", 
                             multicast_group_id="") 

old_devices = old_client.List(old_devices_request, metadata=old_auth_token)

print(f"Devices found on old server:\n{old_devices}")

for device in old_devices.result:
    # Get activation data from old server
    old_activation_request = api.GetDeviceActivationRequest(dev_eui=device.dev_eui)
    activation_data = old_client.GetActivation(old_activation_request, metadata=old_auth_token).device_activation

    # Activate device on the new server using activation_data
    new_activation_request = api.ActivateDeviceRequest(device_activation=activation_data)
    new_client.Activate(new_activation_request, metadata=new_auth_token)




