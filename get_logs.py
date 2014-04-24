from pybeaconclient import PyBeaconClient


if __name__ == '__main__':

    # Lookup device IP
    #sys.stdout.write('Pole Number: ')
    #IP = raw_input()
    IP = '10.0.0.5'

    # Device credentials (should be same on each device)
    user = 'pi'
    pwd = 'greenspace'

    # Create ssh connection
    pybeacon_client = PyBeaconClient(IP, user, pwd)

    # Get logs
    pybeacon_client.get_logs('/home/pi/gspace/src/logs', '../beacon_logs')
