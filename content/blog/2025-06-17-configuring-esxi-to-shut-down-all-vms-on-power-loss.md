---
date: 2025-06-17
lastmod: 2025-06-20
draft: false
slug: configuring-esxi-to-shut-down-all-vms-on-power-loss
title: Configuring ESXi to Shut Down All VMs on Power Loss
description: Notes from an abandoned project to have an ESXi host communicate with the UPS via SNMP. It would then gracefully shut down all VMs and finally itself.
---

{{<notice warning>}}
This post was written at the same time as the project was being researched. Unfortunately, it was discovered too late into the research that ESXi uses RAMdisk and, as a result, nothing persists after a reboot thus adding a major wrench into the mix.

Perhaps there's a utility to mark files/folders as "persist after reboot" or perhaps it's somewhat trivial to create a [vSphere Installation Bundle](https://blogs.vmware.com/vsphere/2011/09/whats-in-a-vib.html) (VIB) for this project. However, it was shelved to focus on the Proxmox migration *(where apcupsd is a thing)*.

Worth checking out:

- https://github.com/rgc2000/NutClient-ESXi
- https://github.com/networkupstools/nut/wiki/NUT-and-VMware-(ESXi)
{{</notice>}}

Rather than setting up every VM in ESXi to monitor the network-connected UPS and shut down when necessary, it would be better if ESXi communicated with the UPS and gracefully shut down every VM and then finally itself. Not to mention that in the former situation, ESXi would then be left running until the power was abruptly cut off.

Installing something on ESXi to communicate with the UPS is *a lot* harder than it should be. One would've thought it would be offered as a native package. Perhaps VMware didn't think power loss would be a thing back in the 6.7 days. Neither do Broadcom today, apparently.

Some suggestions I've found to this common problem:

- **Use an intermediary VM that's responsible for communications between the UPS and ESXi host. When the UPS battery is low, the VM should SSH into the ESXi host to issue the appropriate commands to shut down the VMs and then itself.** That's adding additional dependencies into the mix.
- **vSphere Management Assistant (vMA)**. It provides the functionality; however, it was discontinued in 2017.
- **Use vCenter Server.** I don't want to further complicate things, especially since I'm interested in migrating to Proxmox.
- **Get a generator.** I have a generator. It doesn't help at 3 in the morning.

None of those really fit in line with the current landscape. A more direct approach is taken: ESXi host communicates with the UPS and initiates shutting down when the battery is low. Seems obvious enough.

The idea is to use SSH to create a script on the ESXi 6.7 host to facilitate everything. This script will use SNMP to periodically communicate with a Smart-UPS 1500 unit with an AP9630 Network Management Card (NMC). If the UPS reports the remaining battery level below a certain threshold, gracefully shut down all VMs and finally the host itself.

## SNMP info

Will need to find the OIDs necessary to query the NMC with. For that we'll use [`braa`](https://github.com/mteg/braa). For example, to walk the SNMP tree of host `192.168.1.1` with community string `public` querying all OIDs under `.1.3.6`[^1]:

```bash
braa public@192.168.1.1:.1.3.6.*
```
Will use the OID `.1.3.6.1.4.1.318.1.1.1.2.2.1.0` for the battery capacity.

Here's the list of OIDs for completeness:

| OID | Description | Note |
|-----|-------------|------|
| `.1.3.6.1.4.1.318.1.1.1.1.1.1.0` | UPS type | |
| `.1.3.6.1.4.1.318.1.1.1.2.2.1.0` | Battery capacity percentage | |
| `.1.3.6.1.4.1.318.1.1.1.2.2.2.0` | Internal temperature | In Celsius or Fahrenheit depending on config |
| `.1.3.6.1.4.1.318.1.1.1.2.2.3.0` | Runtime remaining | In milliseconds |
| `.1.3.6.1.4.1.318.1.1.1.2.2.4.0` | Replace batter indicator | 1=ok, 2=replace |
| `.1.3.6.1.4.1.318.1.1.1.3.2.1.0` | Input voltage | |
| `.1.3.6.1.4.1.318.1.1.1.3.2.4.0` | Input frequency | |
| `.1.3.6.1.4.1.318.1.1.1.3.2.5.0` | Reason for last transfer | <ol><li>1 No events</li><li>2 High line voltage</li><li>Brownout</li><li>Loss of mains power</li><li>Small temporary power drop</li><li>Large temporary power drop</li><li>Small spike</li><li>Large spike</li><li>UPS self-test</li><li>Excessive input voltage fluctuation</li></ol> |
| `.1.3.6.1.4.1.318.1.1.1.4.2.1.0` | Output voltage | |
| `.1.3.6.1.4.1.318.1.1.1.4.2.2.0` | Output frequency | |
| `.1.3.6.1.4.1.318.1.1.1.4.2.3.0` | Output load | Expressed as percent of capacity |
| `.1.3.6.1.4.1.318.1.1.1.4.2.4.0` | Output current | Expressed in amps |
| `.1.3.6.1.4.1.318.1.1.1.7.2.3.0` | Last self-test result | 1=pass, 2=fail |
| `.1.3.6.1.4.1.318.1.1.1.7.2.4.0` | Last self-test date | |

## ESXi

The idea is that a script will run periodically on the ESXi host. It will reach out to the UPS via SNMP to query for the remaining battery capacity. If it's below a threshold, then it will shut down all VMs gracefully and then itself.

### SNMP from ESXi

When logging into the ESXi host using SSH for the first time, you might be surprised to learn that it's quite a minimal OS installation.

For one thing, the Net-SNMP tool set isn't available. So the obvious solution of creating a Bash script relying on `snmpget` to query the UPS isn't an option. There is an SNMP daemon that's available, but that doesn't have anything to query external systems with; it's more for external monitoring software to get info about the ESXi host.

For some reason, Python is available (version 3.5), but it might come as no surprise to learn that there's a very limited set of packages installed and pip isn't available[^2]. So that means the recommended ways of using packages aren't available. Writing an SNMP client using raw sockets is definitely out of scope for this project. Another approach to using packages is to download the source code and add that path to `sys.path` so Python knows where to go when loading the module.

Going to use the Python SNMP library, [pysnmp](https://github.com/pysnmp/pysnmp), but we can't use the latest version because it isn't compatible with Python 3.5 due to the use of f-strings, they were introduced in Python 3.6 in [PEP-498](https://peps.python.org/pep-0498/). The most recent version that can be used is 5.0.1. It has a dependency on the ASN.1 library for Python, [pyasn1](https://github.com/etingof/pyasn1). The latest version, 0.4.8, works fine with Python 3.5.

Create a directory for this project and download the libraries from GitHub in there. It should look like this:

```
/
├── upsmon/
|   ├── pyasn1-0.4.8/
|   ├── pysnmp-5.0.1/
|   └── upsmon.py
```

While it's rather verbose, leaving the version numbers in the directory names for the libraries adds a little to the documentation.

### The Script

To use the downloaded Python libraries stored in the non-standard location, you'll need to add their paths so the script knows where to go to load them. Start the Python script with this:

```python
import sys

sys.path.append('pyasn1-0.4.8')
sys.path.append('pysnmp-5.0.1')
```

*There were a few basic Python scripts iterating on the complete solution, but they were all lost after the first reboot and the discovery of RAMdisk. Follow the examples in the docs for pysnmp.*

The crontab for root is located at `/var/spool/cron/crontabs/root`

[^1]: You're going to get a few notifications from the UPS about "Detected an unauthorized user attempting to access the SNMP interface" unless you add your machine's IP in the SNMP Access Control of the UPS for the community name. It's relatively safe to ignore these notifications otherwise though.
[^2]: Forget about installing pip. The `get-pip.py` script from https://bootstrap.pypa.io/pip/3.5/get-pip.py (the last version that supports Python 3.5) ultimately fails with a "Could not find a version that satisfies the requirement pip<21.0" error message. The standalone `pip.pyz` application fails with "This version of pip does not support python 3.5 (requires >= 3.9)."
