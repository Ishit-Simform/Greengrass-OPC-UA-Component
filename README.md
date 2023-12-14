# Greengrass OPC UA Component

This component provides the ability to read device data using OPC UA protocol.<br>

## Installation

Configure the recipe template and deploy the component to greengrass core device.

### Recipe configuration

Edit the following placeholders in recipe template.

- `<policy>`: Policy could be ``Basic128Rsa15``, ``Basic256`` or ``Basic256Sha256``.
- `<security_mode>`: Security Mode could be ``Sign`` or ``SignAndEncrypt`` or ``None``.
- `<certificate_path>`: Specify the full path of certificate.
- `<privatekey_path>`: Specify full path of private key.
- `<kepware_endpoint>`: Specify Kepware endpoint mentioned in Kepware Configuration.
- `<kepware_name>`: Specify name of kepware channel name that consists devices.
- `<devices>`: You could list multiple devices with device name and parameters.
    - `<device_name>`: Unique device name as specified in Kepware.
    - `<parameters>`: Parameters of this device as specified in Kepware.

## Usage

#### Example
```
"policy": "Basic256Sha256",
"security_mode": "SignAndEncrypt",
"certificate_path": "/home/pi/certificate-example.der",
"privatekey_path": "/home/pi/private-key-example.pem",
"kepware_endpoint": "opc.tcp://127.0.0.1:49320/KEPServerEX/", 
"kepware_name": "PLC_simulator_script",      
"devices": [
{
    "device_name": "Device1",          
    "parameters": [
    "Tension pot position",
    "Nip Pressure",
    "Mercerisation Bath Temp",
    "Mercerisation Bath pH",
    "Hot bath Temp",
    "Hot bath pH",
    "Cold bath Temp",
    "Cold bath pH",
    "Dye Dosage",
    "Hydro Dosage",
    "Steam Pressure",
    "Waste water out flow",
    "Rope Out Speed",
    "Mercerisation Bath",
    "Mercerisation Hot Bath",
    "Mercerisation Cold Bath",
    "Mercerisation Bath Hydro concetration",
    "Mercerisation Hot Bath Hydro concetration",
    "Mercerisation Cold Bath Hydro concetration",
    "Totalizer",
    "Rinse cycle",
    "Dye bath Filteration"
    ]
},
{
    "device_name": "Device2",          
    "parameters": [
    "Dancer Position",
    "Beam Length Meter",
    "Speed",
    "Comb Acentric",
    "Strummer",
    "Air blower",
    "Lease string detector",
    "Accumulator Motor"            
    ]
},
{
    "device_name": "Device3",          
    "parameters": [
    "Dancer Position",
    "Beam Length Meter",
    "Speed",
    "Comb Acentric",
    "Strummer",
    "Air blower",
    "Lease string detector",
    "Accumulator Motor"            
    ]
},
{
    "device_name": "Device4",          
    "parameters": [
    "Dancer Position",
    "Beam Length Meter",
    "Speed",
    "Comb Acentric",
    "Strummer",
    "Air blower",
    "Lease string detector",
    "Accumulator Motor"            
    ]
},
{
    "device_name": "Device5",          
    "parameters": [
    "Dancer Position",
    "Beam Length Meter",
    "Speed",
    "Comb Acentric",
    "Strummer",
    "Air blower",
    "Lease string detector",
    "Accumulator Motor"            
    ]
}
]
```