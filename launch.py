import orbitalweapons.server

app = flask.Flask(__name__)

"""
 ______                        __          _                   
|_   _ `.                     [  |        / |_                 
  | | `. \ .---.  .--.   .--.  | |  ,--. `| |-' .--.   _ .--.  
  | |  | |/ /__\\( (`\]/ .'`\ \| | `'_\ : | | / .'`\ \[ `/'`\] 
 _| |_.' /| \__., `'.'.| \__. || | // | |,| |,| \__. | | |     
|______.'  '.__.'[\__) )'.__.'[___]\'-;__/\__/ '.__.' [___]    
"""                                                         

# Check sattelite status
@app.route('/api/v3/fire', methods=['GET'])
def status():
    # TODO - password protection

    # 03/21/2021 - pass protection pushed to next development sprint per solper's request
    # 04/25/2021 - brough up the pass protection in team standup. CTO asked to postpone further
    # 06/10/2021 - we have a pentest scheduled for next month and our firing endpoint is unprotected
    # 06/10/2021 - if we do not implement this ASAP, people will get hurt

    #password = 'tsctf{misfire_was_no_coincidence}'

    try:
        # if we have authorization, go ahead and fire
        if authorized == true:
            return '[+] Launch inbound. Brace for impact'
        else:
            # if not, return an error
            return '[-] Error, no authorization provided, override required'
    except Exception as exception_message:
        return '[!] The following exception has occured: {}'.format(exception_message)

# Enable the sattelite uplink
@app.route('/api/v3/override', methods=['GET'])
def enable():
    # per CTO's request, i first encoded, then scrambled and then encoded the override code download password
    # override_download_pw = '011100010101010101000001011101110111000101010100010011010011011101110000001100100101001100110001011011110101001100111001011011010110111100110010011010110110101001001101010010110101011101110011011011100100101101000001011100110111000000110011010010010110110101110011010001000011110100111101'
    override_pw = 'REDACTED'

    # TODO - check the override password itself
    # WARNING - THE CODE IS EXPERIMENTAL. DO NOT USE IN PROD YET.
    try:
        if 'code' in request.args:
            provided_code = str(request.args['code'])
            if provided_code == override_pw:
                uplink_enabled = True
                client_ip = str(request.remote_addr)
                return '[+] Success: Override Enabled [+]'
            else:
                return '[!] Error: Invalid Override Code [!]'
        else:
            return '[!] Error: Please provide an Override code [!]'
    except Exception as exception_message:
        return '[?] The following exception has occured: {}'.format(exception_message)

app.run(host='0.0.0.0')