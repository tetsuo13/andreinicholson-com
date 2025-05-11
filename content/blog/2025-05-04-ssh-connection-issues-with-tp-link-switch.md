---
date: 2025-05-04
lastmod: 2025-05-04
draft: false
slug: ssh-connection-issues-with-tp-link-switch
title: SSH Connection Issues with TP-Link Switch
description: A series of issues connecting to an older TP-Link switch using SSH from a newer client. And some solutions, too.
---

While the initial problem was encountered trying to connect to a TP-Link T1600G switch after a reset and running the latest firmware, the issues encountered in this post can originate from just about any older piece of hardware.

## Connections issues

All the customizations required to successfully connect via SSH were isolated to `~/.ssh/config` and *just to this one host* since the intention is to use less secure methods. This is the final result:

```sshconfig
Host 192.168.0.1
    KexAlgorithms +diffie-hellman-group1-sha1
    Ciphers +aes128-cbc,aes192-cbc,aes256-cbc
    HostKeyAlgorithms +ssh-dss
    PubkeyAuthentication no
    PreferredAuthentications password
```

### Unable to negotiate

When attempting to SSH into the switch, you may encounter this error:

> Unable to negotiate with 192.168.0.1 port 22: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1

While there's a helpful starter FAQ page on TP-Link's website on this subject, [How to configure OpenSSH 7.0(and above) to login smart and managed switches](https://www.tp-link.com/en/support/faq/2025/)[^1], it didn't resolve my issue as that led to the next error with the cipher:

> Unable to negotiate with 192.168.0.1 port 22: no matching cipher found. Their offer: aes128-cbc,aes192-cbc,aes256-cbc,blowfish-cbc,cast128-cbc,3des-cbc

To make an exception for allowing the older and less secure connection method, create an entry for the switch in your OpenSSH client config file. Open `~/.ssh/config` and add the following lines:

```sshconfig
Host 192.168.0.1
    KexAlgorithms +diffie-hellman-group1-sha1
    Ciphers +aes128-cbc,aes192-cbc,aes256-cbc
    HostKeyAlgorithms +ssh-dss
```

This will configure the SSH client to use this less secure connection method. The list of key exchange algorithms and ciphers were derived by scanning the host and using the first few listed:

```
$ nmap --script ssh2-enum-algos 192.168.0.1
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-05-05 04:03 UTC
Nmap scan report for 192.168.0.1
Host is up (0.082s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERVICE
22/tcp  open  ssh
| ssh2-enum-algos:
|   kex_algorithms: (1)
|       diffie-hellman-group1-sha1
|   server_host_key_algorithms: (1)
|       ssh-dss
|   encryption_algorithms: (6)
|       aes128-cbc
|       aes192-cbc
|       aes256-cbc
|       blowfish-cbc
|       cast128-cbc
|       3des-cbc
|   mac_algorithms: (4)
|       hmac-sha1
|       hmac-sha1-96
|       hmac-md5
|       hmac-md5-96
|   compression_algorithms: (1)
|_      none
80/tcp  open  http
443/tcp open  https

Nmap done: 1 IP address (1 host up) scanned in 2.41 seconds
```

### Connection closed

The remote connection is immediately closed after connecting to the host:

```
$ ssh admin@192.168.0.1
Connection closed by 192.168.0.1 port 22
```

Increasing the verbosity and looking at the last few lines of the output to get a better idea of what's happening:

```
$ ssh -v admin@192.168.0.1
...
Authenticated using "none" with partial success.
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: get_agent_identities: bound agent to hostkey
debug1: get_agent_identities: agent returned 1 keys
...
debug1: Offering public key
Connection closed
```

The line with "Authentications that can continue: publickey,password" is noteworthy here. It states the authentication methods accepted in order. The client sees "publickey" first, and so it attempts to perform public key authentication but fails because the public key file hasn't been imported on the switch. Force password authentication by adding the following lines for the host:

```sshconfig
Host 192.168.0.1
    PubkeyAuthentication no
    PreferredAuthentications password
```

See TP-Link's [Configuration Guide for Accessing the Switch Securely](https://www.tp-link.com/us/configuration-guides/configuration_guide_for_accessing_the_switch_securely/) on how to configure the switch between password and key authorization modes in case passwords isn't something you want to use in which case *don't* add the above lines.

[^1]: Don't make the suggested changes to the system's `/etc/ssh/ssh_config` file. It's best to keep edits contained to your home directory instead.
