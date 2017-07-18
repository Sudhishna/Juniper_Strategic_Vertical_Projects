from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import jcs
import re
 
def main():
    dev = Device()
    dev.open()
    routeConf=dev.cli("show config routing-options static",warning=False)
    routeCli=dev.cli("show route protocol static",warning=False)
 
    subnet_desc = {}
 
    filelines=re.split("\n",routeConf)
    for line in filelines:
        regex_pattern = re.search('\/\*(\w*.*)\*\/',line)
        if(regex_pattern):
            description=regex_pattern.group(1)
        regex_pattern = re.search('^\s*route\s*(\d+\.\d+\.\d+\.\d+\/\d+)',line)
        if(regex_pattern and description):
            subnet=regex_pattern.group(1)
            subnet_desc[subnet]=description
            description=None
 
    filelines=re.split("\n",routeCli)
    for line in filelines:
        regex_pattern = re.search('^\s*(\d+\.\d+\.\d+\.\d+\/\d+)\s*.*Static',line)
        if(regex_pattern):
            route=regex_pattern.group(1)
            if route in subnet_desc.keys():
                print line + " /*" + subnet_desc[route] + "*/"
            else:
                print line
        else:
            print line
 
    dev.close()
 
if __name__ == "__main__":
    main()
