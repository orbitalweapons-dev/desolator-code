$desolator_ip = Read-Host "[?] Please enter the IP of the Desolator: "
$authorization_code = 'REDACTED'
curl "${desolator_ip}:5000/api/v3/authorize?code=${authorization_code}"
Read-Host -Prompt “Press Enter to exit”
