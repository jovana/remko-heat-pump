# REMKO.de Heat Pump - API

If your REMKO Heat Pump has a SmartControl interface and it has connected to your lan network. You can send POST commands to control the settings.

## REMKO WKF-Compact
This manual has been tested on a WKF120 device, running software version 4.23.
https://www.remko.de/en/products/new-energies/smart-heat-pumps/wkf-compact-series/



## Example commands (using curl)
In the below examples you need to replace <YOUR_IP_ADDRESS> first. This IP address you can found in the settings section of your device.

### Switch OFF the Domestic Hot Water Heating
```
curl --request POST \
  --url 'http://<YOUR_IP_ADDRESS>/cgi-bin/webapi.cgi' \
  --header 'Content-Type: application/json' \
  --data '{"SMT_ID": "0000000000000000","query_list":[1079],"values": {"1079":"03"}}'
```

### Switch standby the Heating / Cooling mode
```
curl --request POST \
  --url 'http://<YOUR_IP_ADDRESS>/cgi-bin/webapi.cgi' \
  --header 'Content-Type: application/json' \
  --data '{"SMT_ID": "0000000000000000","query_list":[1088],"values": {"1088":"03"}}'
```

## REMKO Command table (version 4.23)
The below codes are used the get and set parameters to your device.
|REMKO Code   | Paramater | Description      |
|-------------|------------|-----------------|
| 1079        | 00 | Domestic Hot Water - Auto Comfort  |
| 1079        | 01 | Domestic Hot Water - Auto eco  |
| 1079        | 02 | Domestic Hot Water - Solar / pv  |
| 1079        | 03 | Domestic Hot Water - Off  |
| 1088        | 01 | Heating / Cooling - Automatic  |
| 1088        | 02 | Heating / Cooling - Heating  |
| 1088        | 03 | Heating / Cooling - Standby  |
| 1088        | 04 | Heating / Cooling - Cooling  |
