#!/usr/bin/python
# coding: utf-8
#
# Create objects in Panorama woth pandevice framework
# https://github.com/PaloAltoNetworks/pandevice
#
# Features (use --help for usage help):
#   - Create objects in shared from imput variables
#   - Modify objects if they already exists
#   - Delete objects
#
# Author:   Philippe Glohr
# Date:     2018-10
# Version:  0.01 @ 20181029

import argparse
import pandevice
from pandevice import panorama
from pandevice import objects
from IPython import embed

# Fixed variables
PAN_IP_address = "panorama_hostname"
PAN_API_KEY = "API-key"
pano = panorama.Panorama(PAN_IP_address, api_key=PAN_API_KEY)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd', type=str, help='Operation (Add, Mod or Del)', required=True)
    parser.add_argument('--name', type=str, help='Object name', required=True)
    parser.add_argument('--ip', type=str, default='', help='Object IP address')
    parser.add_argument('--type', type=str, default='fqdn', help='Object type fqdn or ip-netmask')
    parser.add_argument('--desc', help="Object description")    
    parser.add_argument('--tag', help="List of tags separated with ,")    
    args = parser.parse_args()

	# Variables coming from ITEMS system
    var_host_name = "H_"+args.name
    var_host_name_length = len(var_host_name)
    # Set correct format of "var_host_ip" variable based on object type (IP or fqdn)
    if args.type == 'ip-netmask':
        var_host_ip = args.ip+"/32"
    else:
        var_host_ip = args.ip
	
	# Check hostname length
    if len(var_host_name) < 64:
        if args.cmd == 'Add':
    		# This call allow to create the object and modify IP address or description if the host already exist
            webserver = objects.AddressObject(var_host_name, var_host_ip, type=args.type, description=args.desc, tag=tuple(args.tag.split(',')))
#            pano.find(panorama.DeviceGroup("DG_GDC_MGMT_Zone"))
            pano.add(webserver)
            webserver.create()
			# embed()
            pano.commit()
            print (webserver)

        elif args.cmd == 'Del':
    		# This call allow to delete the host
            webserver = objects.AddressObject(var_host_name)
            pano.add(webserver)
            webserver.delete()
            # embed()
            pano.commit()
            print (webserver)

        elif args.cmd == 'Mod':
		    # This call allow to update the tags
            webserver = objects.AddressObject(var_host_name, var_host_ip, description=args.desc, tag=tuple(args.tag.split(',')))
            pano.add(webserver)
            webserver.apply()
            pano.commit()
            # embed()
            print (webserver)

    else:
        print ("Host name exceed 63 character")

