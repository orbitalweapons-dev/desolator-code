$desolator_ip = Read-Host "[?] Please enter the IP of the Desolator: "
$authorization_code = '4a2dbd905287e75a5d2b659d2546fbab79abb21689e50f59492612df59bff460'
curl "${desolator_ip}:5000/api/v3/authorize?code=${authorization_code}"
Read-Host -Prompt “Press Enter to exit”