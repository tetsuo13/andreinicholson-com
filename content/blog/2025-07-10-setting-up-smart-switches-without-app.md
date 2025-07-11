---
date: 2025-07-10
lastmod: 2025-07-10
draft: false
slug: setting-up-smart-switches-without-app
title: Setting up Smart Switches Without an App
description: Small collection of notes on how to set up several smart switches on Wi-Fi without having to use their app.
---

This is a collection of notes on how to perform the initial setup for several different smart switches without the use of their proprietary apps. The goal is just to get the device on my Wi-Fi, after that Home Assistant will take care of the rest.

Typically, the setup process would be to install the app on my phone, set up an account, discover the device, set it up on my Wi-Fi, then uninstall the app. Even though it's minimal use of the app, I want to avoid it because I don't like signing up for accounts, and often these apps require granting location access and other seemingly nonrelated permissions during the setup process. All of this seems entirely unnecessary and more like I'm feeding more data out there that will get leaked at some point anyway.

## Belkin WeMo Mini Smart Plug

For the WeMo Mini Smart Plug devices, use the [pyWeMo Python library](https://github.com/pywemo/pywemo) to set them up.

You can tell the difference between the F7C063 models by the presence of the Apple HomeKit sticker on the back. Only the 2nd gen models have it.

A reference to the different states of the status light, from the [Understanding the Wemo Mini Smart Plug, F7C063 Status Light](https://www.belkin.com/support-article/?articleNum=226106) page at Belkin:

- **Blinking white**: When first plugged in and is starting up. Should last about 15 seconds.
- **Solid white**: When the device is configured, working properly, and has power.
- **Blinking orange**: The device has Wi-Fi configuration but is unable to connect.
- **Solid orange**: Connected to Wi-Fi but has a poor signal.
- **Alternating white/orange**: The device has finished booting up and is ready for setup.
- **Off**: Device is off and functioning as normal.

### Model F7C063 (2nd gen)

The [F7C063](https://www.belkin.com/support-article/?articleNum=226110) model is fairly reliable and relatively easy to manage.

Start by resetting the device and putting it into the setup mode. Reset it by holding down the button for 5 seconds while the device is plugged in. You should see the status light flash quickly a few times and then settle into its slowly alternating white/orange blinking indicating that it's not connected to any SSID.

Now connect to the device to manage it. Look for a Wi-Fi SSID like "Wemo.Mini.xxx" where the last part is a three-digit number. It'll be an open access point. Connect to that SSID.

Use a Python prompt to find the device:

```python
>>> import pywemo
>>> devices = pywemo.discover_devices()
>>> print(devices)
[<WeMo Switch "Wemo Mini 4">]
```

To verify you're connected to the switch you think you're connected to, you can toggle it with:

```python
devices[0].toggle()
```

Set it up on the new SSID:

```python
devices[0].setup(ssid='SSID-GOES-HERE', password='PASSWORD-GOES-HERE')
```

After a few seconds you should be disconnected from the WeMo access point, the blinking status light should stop blinking, and eventually the Python command will start showing errors:

> Error communicating with Wemo Mini 4 at 10.22.22.1:49152, HTTPException(MaxRetryError("HTTPConnectionPool(host='10.22.22.1', port=49152): Max retries exceeded with url: /upnp/control/WiFiSetup1 (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x7bd87f05c950>, 'Connection to 10.22.22.1 timed out. (connect timeout=3.0)'))")) retry 0
>
> Unable to re-probe wemo <WeMo Switch "Wemo Mini 4"> at 10.22.22.1
>
> Unable to reconnect with Wemo Mini 4

You can press `Ctrl+C` to cancel further retries since they will also fail because the device should now be connected to the SSID specified in the `setup` call.

Some potential errors:

**WeMo device failed to connect byt has status=3**

> pywemo.exceptions.SetupException: Wemo device failed to connect to "SSID-GOES-HERE", but has status=3,which usually precedes a successful connection.  Thus it may still connect to the network shortly.  Otherwise, please try again.

The device will successfully connect to Wi-Fi but will be unresponsive from Home Assistant and the status light will continue with the alternating white/orange blinking. Reset the device and try again.

**AP with SSID not found**

> pywemo.exceptions.APNotFound: AP with SSID SSID-GOES-HERE not found.  Try again.

Try the `setup` call again. You may encounter this error several times.

### Model WSP080

The [WSP080](https://www.belkin.com/support-article?articleNum=317057) model has been unbelievably unreliable. They become unresponsive, either dropping from Wi-Fi and not reconnecting or even the button on the device itself not functioning. It requires physically reseating the device in the outlet to overcome. This happens about every 2 days on average. I purchased a single three-pack and witnessed this behavior on each of them. Perhaps it was a faulty batch that could've been fixed with a firmware update, but, they're junk.

It's possible that the same process as the F7C063 will work. The Wi-Fi SSID on this device will be something like "Wemo.Plug.xxx".

## TP-Link Kasa Smart Wi-Fi Plug Mini (model HS103)

Use the [python-kasa Python library](https://python-kasa.readthedocs.io/) to set them up.

The [support page at TP-Link](https://www.tp-link.com/us/support/download/hs103/) is a great resource for everything you need to know.

Reset the device by holding the control button for 10 seconds. The status light should be alternating blue/amber. Now connect to the device to manage it. Look for a Wi-Fi SSID like "TP-LINK_Smart Plug_xxxx" where the last part is the last two octets of the MAC address. It'll be an open access point.

Find the device with

```
$ ./kasa discover
Discovering devices on 255.255.255.255 for 10 seconds
== TP-LINK_Smart Plug_ABCD - HS103 ==
Host: 192.168.0.1
Port: 9999
Device state: True
Time:         2000-01-01 16:56:02-08:00 (tz: PST8PDT)
Hardware:     5.0 (US)
Firmware:     1.0.3 Build 201015 Rel.142523
MAC (rssi):   28:87:BA:AA:BB:CC (-46)

== Primary features ==
State (state): True

== Information ==
On since (on_since): 2000-01-01 16:00:00-08:00
Cloud connection (cloud_connection): False

== Configuration ==
LED (led): True

== Debug ==
RSSI (rssi): -46 dBm
Reboot (reboot): <Action>

Found 1 devices
```

Note the host address, `192.168.0.1` in this case.

Scan for available networks to join with the `kasa wifi` command:

```
$ ./kasa --host 192.168.0.1 wifi scan
Discovering device 192.168.0.1 for 10 seconds
Scanning for wifi networks, wait a second..
Found 7 wifi networks!
	 WifiNetwork(ssid='2WIRE199', key_type=3, cipher_type=None, bssid=None, channel=None, rssi=None, signal_level=None)
	 WifiNetwork(ssid='NETGEAR42', key_type=4, cipher_type=None, bssid=None, channel=None, rssi=None, signal_level=None)
	 WifiNetwork(ssid='Marriott_Guest', key_type=3, cipher_type=None, bssid=None, channel=None, rssi=None, signal_level=None)
	 WifiNetwork(ssid='Bob', key_type=4, cipher_type=None, bssid=None, channel=None, rssi=None, signal_level=None)
```

Note the `key_type` value for the SSID to join, you'll be prompted for it in the next command.

Join the network with:

```
./kasa --host 192.168.0.1 --type plug wifi join 2WIRE199
Keytype: 3
Password:
Asking the device to connect to 2WIRE199..
Response: {} - if the device is not able to join the network, it will revert back to its previous state.
```

The status light will change to solid blue, and you will be kicked off of the device's Wi-Fi as it should now be connected to the SSID specified.
