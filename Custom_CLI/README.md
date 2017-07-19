Loading Yang and Python Script for the new CLI:
----------------------------------------------
 
YANG module, action script, and required extension modules to the device (to /var/tmp)
4 files need to be copied to /var/tmp/ 
1. YANG Module- static-route-desc.yang
2. ACTION SCRIPT -> static-route-desc.py
3. Junos Modules -> junos-extension.yang
4. junos-extension-odl.yang

To get the junos modules you can use the below command.
show system schema module junos-extension format yang output-directory /var/tmp/
show system schema module junos-extension-odl format yang output-directory /var/tmp/

CLI> request system yang validate module /var/tmp/static-route-desc.yang action-script /var/tmp/static-route-desc.py
CLI> request system yang add package intf-rpc module [/var/tmp/ static-route-desc.yang /var/tmp/junos-extension.yang /var/tmp/junos-extension-odl.yang] action-script /var/tmp/ static-route-desc.py
        Restart cli? Yes <enter>

CONFIG> set system scripts language python
CONFIG> commit and-quit

CLI > show stat-route des   
 inet.0: 7 destinations, 7 routes (7 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both
0.0.0.0/0          *[Static/5] 00:01:52 /* Test Description 1 */
                     > to 192.168.122.1 via fxp0.0
130.0.0.0/8        *[Static/5] 00:01:52 /* Test Description 2 */
                     > to 192.168.122.1 via fxp0.0
140.0.0.0/8        *[Static/5] 00:01:52 /* Test Description 3 */
                     > to 192.168.122.1 via fxp0.0

I’ve written a python Op Script to add the description to the STATIC Routes.
---------------------------------------------------------------------------
 
The customer can now add descriptions to the Routes using annotate and view them using Python Op Script.
 
Static Routes:
root# show routing-options
static {
    /* The New Description */
    route 0.0.0.0/0 next-hop 192.168.122.1;
    route 138.0.0.0/8 next-hop 192.168.122.1;
    route 140.0.0.0/8 next-hop 192.168.122.1;
}

 
Add Description to the route:
[edit routing-options static]
root# annotate route 138.0.0.0/8 "Test Desciption 1"
root# show
/* The New Description */
route 0.0.0.0/0 next-hop 192.168.122.1;
/* Test Desciption 1 */
route 138.0.0.0/8 next-hop 192.168.122.1;
route 140.0.0.0/8 next-hop 192.168.122.1;
 
Import Op Script:
Copy the below Op Script to the directory “/var/db/scripts/op/”
[edit system scripts op]
user@host# set file config-change.py
 
[edit system scripts]
user@host# set language python
 
[edit]
user@host# commit and-quit
 
Run the Op Script for desired output:
user@host> op StaticDesc.py
 
The customer can now see the Static Routes with its description, if any.
Checked all the corner cases as well.
