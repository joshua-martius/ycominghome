# ycominghome
Automatically turns off hue lighting when certain devices (typically phones) arent in wifi anymore

# Requirements
## Modules
pip3 install phue

## config.json
```json
{
    "atHome": false,
    "devices": [
        ""
    ],
    "sleeptime": 10,
    "groupsToTurnOn": [
        ""
    ],
    "bridgeAddress": "",
    "timeUntilTimeOut": 1.0
}
```
Get config.json via terminal:
```bash
$ curl https://pastebin.com/raw/mbW9EJpr > config.json
```
