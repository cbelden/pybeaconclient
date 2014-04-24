from pybeaconclient import PyBeaconClient
import sys
import getpass


if __name__ == '__main__':

    # Get device IP
    sys.stdout.write('IP: ')
    IP = raw_input()

    # Device credentials (should be same on each device)
    sys.stdout.write('Username: ')
    user = raw_input()
    pwd = getpass.getpass()

    # Create ssh connection
    pybeacon_client = PyBeaconClient(IP, user, pwd)

    # Get logs
    pybeacon_client.get_logs('/home/pi/gspace/src/logs', '../beacon_logs')
