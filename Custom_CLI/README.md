Custom CLI:
------------
 
Copy junos modules to the device (to /var/tmp) using:
--------------------
show system schema module junos-extension format yang output-directory /var/tmp/

show system schema module junos-extension-odl format yang output-directory /var/tmp/

Copy YANG module and action script from GIT to the device (to /var/tmp)
----------------------

a. YANG Module- static-route-desc.yang

b. ACTION SCRIPT -> static-route-desc.py

Load them modules and scripts into the device:
---------------------
CLI> request system yang validate module /var/tmp/static-route-desc.yang action-script /var/tmp/static-route-desc.py

CLI> request system yang add package intf-rpc module [/var/tmp/ static-route-desc.yang /var/tmp/junos-extension.yang /var/tmp/junos-extension-odl.yang] action-script /var/tmp/ static-route-desc.py

Restart cli? Yes <enter>

Enable Python Scripts:
----------------
CONFIG> set system scripts language python

CONFIG> commit and-quit

Check Output:
---------
CLI > show stat-route des   

 inet.0: 7 destinations, 7 routes (7 active, 0 holddown, 0 hidden)

+ = Active Route, - = Last Active, * = Both

0.0.0.0/0          *[Static/5] 00:01:52 /* Test Description 1 */

                     > to 192.168.122.1 via fxp0.0

130.0.0.0/8        *[Static/5] 00:01:52 /* Test Description 2 */

                     > to 192.168.122.1 via fxp0.0

140.0.0.0/8        *[Static/5] 00:01:52 /* Test Description 3 */

                     > to 192.168.122.1 via fxp0.0

