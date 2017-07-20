Event-Policy Configuration:
----------------
Event:
-------
set snmp rmon alarm 1 interval 10

set snmp rmon alarm 1 variable jnxOperatingCPU.9.1.0.0

(in the above config, if you have to find which variable you should be monitoring in your corresponding device, use the command “show snmp mib walk jnxOperatingDescr | match Routing”)

set snmp rmon alarm 1 sample-type absolute-value

set snmp rmon alarm 1 rising-threshold 80

set snmp rmon alarm 1 rising-event-index 1

set snmp rmon event 1 type log
 
Policy:
-------
set event-options policy test events snmpd_rmon_eventlog

set event-options policy test then execute-commands commands "show system uptime |no-more"

set event-options policy test then execute-commands commands "show chassis routing-engine |no-more"

set event-options policy test then execute-commands commands "show system processes extensive |no-more"

set event-options policy test then execute-commands output-filename CPU-GET-HIGH.txt

set event-options policy test then execute-commands destination log-for-CPU-GET-HIGH

set event-options policy test then execute-commands output-format text

set event-options destinations log-for-CPU-GET-HIGH archive-sites scp://ssendhil@192.168.20.2/var/log/cpu_high" password "salt123"
 
commit above changes

To check the events raised from within the device you can use “show snmp rmon logs” (whenever the cpu goes beyond 80%, event is generated)
 
SNMP RMON
--------
https://www.juniper.net/techpubs/en_US/junos/topics/reference/configuration-statement/alarm-edit-snmp.html

Event Policy
----------
https://www.juniper.net/documentation/en_US/junos12.3/topics/topic-map/junos-script-automation-event-policy-change-configuration.html
 
 
Proxy Minion:
--------
One proxy minion per Juniper Device. No limit to the number of proxy-minions one can have.
 
>sudo cat /srv/pillar/top.sls
base:
  'EX2200-D1_192_168_20_1':
    - EX2200-D1_192_168_20_1
 
>sudo cat /srv/pillar/EX2200-D1_192_168_20_1.sls
proxy:
  proxytype: junos
  host: 192.168.20.1
  username: root
  passwd: salt123
 
Event Monitoring:
---------------
You have to setup Beacons in SaltStack to monitor the events coming from the juniper device. (/etc/salt/minion)
beacons:
    var/log/cpu_high:
      mask:
        - create
 
Reactor System
--------------
>sudo cat /etc/salt/master.d/reactor.conf
runner_dirs: [/srv/runners]
reactor:
- salt/beacon/SaltStackMinion/inotify/var/log/cpu_high:
    - /srv/reactor/cpuhigh.sls
 
>sudo cat /srv/reactor/cpuhigh.sls
cpuhigh:
  runner.cpuhigh.infoCollect:
    - user: root
    - event_tag: {{ tag }}
    - event_data: {{ data }}
 
The final python script that gets invoked is the /srv/runners/cpuhigh.py. (In Attachments).
 
More info about the Proxy Minions, Beacons  and Reactors:
---------------------
Proxy Minion:
https://docs.saltstack.com/en/latest/topics/proxyminion/index.html#configuration-parameters
Beacons:
https://docs.saltstack.com/en/latest/topics/beacons/index.html
Reactors:
https://docs.saltstack.com/en/latest/topics/reactor/
