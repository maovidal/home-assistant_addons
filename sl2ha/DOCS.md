# Home Assistant Add-on: SL2HA add-on

This is meant to be used as a [Home Assistant](https://www.home-assistant.io) add-on.


## Description

SL2HA (Syslog to Home Assistant) acts as a very simple [Syslog server](https://en.wikipedia.org/wiki/Syslog) just listening for logs at the configured port.

Once a part of the content received matches an specified string, it fires a POST request to the [REST API](https://developers.home-assistant.io/docs/api/rest/) using the specified ENDPOINT and JSON PAYLOAD.


## Examples

### Detecting an incoming phone call from a telephony gateway

The [legacy OBI100/110 telephony gateways](https://www.callcentric.com/support/device/obihai/obi100) are able to provide their logs when enabling this function at 'System Management' >> 'Device Admin' >> Syslog.

The SL2HA add-on can have the following configuration to turn on a Home Assistant input_boolean named 'doorman' when the log received from the OBI110 tells that there is an incoming call from its land line:

    endpoint_1: "states/input_boolean.doorman"
    to_seek_1: "[DAA]: FXO ring on"
    payload_1: '{"state": "on"}'

To turn off the 'doorman', the following configuration can be used:

    endpoint_2: "states/input_boolean.doorman"
    to_seek_2: "[DAA]: FXO ring off"
    payload_2: '{"state": "off"}'

*Please note that payload_1 and payload_2 are JSON strings and should be escaped correctly.*


## Support and contribution

The easiest way to check the operation of this addon is checking its own logs.
By default those are in INFO mode and provide basic details, like the current configuration as seen by the Python script.

To get a deeper details, the DEBUG mode can be enabled using that flag on the addon configuration.

Please open an issue here on GitHub if you need support.

Pull requests are welcome.


## Authors & contributors

The original setup of this repository is by Mauricio Vidal.

The part related to the "Syslog Server" is based on: https://gist.github.com/marcelom/4218010
