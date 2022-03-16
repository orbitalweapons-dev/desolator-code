#!/bin/bash
echo '[?] Please enter the IP of the Desolator: '
read desolator_ip
uplink_code='redacted'
host=$(hostname -I)
curl "${desolator_ip}:5000/api/v3/enable?code=${uplink_code}&host=${host}"
