import paramiko
import os
import errno
from datetime import datetime


class PyBeaconClient():
    """Communicates with a trackr device."""

    def __init__(self, IP, username, password):
        """Initializes the PyBeaconClient instance."""

        # Initialize/Configure ssh to auto-connect to unknown IPs
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to device
        try:
            self._ssh.connect(IP, username=username, password=password)
        except Exception:
            print 'Could not connect to device: ' + IP
            print 'Check if connected to network correctly.'
            exit(-1)

    def download_logs(self, devicepath, localpath, delete=False):
        """Retrieves the beacon logs stored on the logging device at devicepath and stores them locally in localpath."""

        # Format paths
        devicepath = devicepath.rstrip('/')
        localpath = localpath.rstrip('/')

        # Ensure devicepath exists
        self._devicepath_exists(devicepath)

        # Get log directories (one for each day EXCEPT most recent)
        stdin, stdout, stderr = self._ssh.exec_command('ls ' + devicepath)
        logfolders = [d.rstrip() for d in stdout.readlines()[:-1]]
        print 'Found ', len(logfolders), ' to retrieve..'

        # Create local log folders
        self._create_log_folders(localpath, logfolders)

        # Download each subdirectory in the main log directory
        for logfolder in logfolders:
            print 'Retrieving log folder: ' + logfolder + ' ...'
            self._download_log_folder(devicepath, logfolder, localpath)

    def set_utc_date(self):
        """Sets the device's utc date to the local utc date."""

        utc_date = str(datetime.utcnow())

        # Strip millisecond data
        utc_date = utc_date.split('.')[0]

        stdin, stdout, stderr = self._ssh.exec_command('sudo date -s "' + utc_date + '" -u')

    def delete_logs(self, devicepath, logdirs):
        """Deletes all of the specified log directories."""
        pass

    def _download_log_folder(self, devicepath, log, localpath):
        """Stores log .txt files in logpath in the directory specified by localpath."""

        logpath = '/'.join([devicepath, log])
        stdin, stdout, stderr = self._ssh.exec_command('ls ' + logpath)
        log_files = [l.rstrip() for l in stdout.readlines()]

        # Open sftp connection
        sftp = self._ssh.open_sftp()

        for f in log_files:
            src = '/'.join([logpath, f])
            target = '/'.join([localpath, log, f])

            print '\tfetching file: ' + f + '...'

            try:
                sftp.get(src, target)
            except Exception:
                print '*** Error copying ' + src + ' to ' + target

        sftp.close()

    def _devicepath_exists(self, path):
        """Ensures the specified device path exists."""

        sftp = self._ssh.open_sftp()

        try:
            sftp.stat(path)
        except IOError, e:
            if e.args[0] == errno.ENOENT:
                print "Device path does not exist"
                raise e

        sftp.close()

    def _create_log_folders(self, localpath, logfolders):
        """Generates a local log directory in localpath for each directory in logfolders."""

        for logfolder in logfolders:
            path = '/'.join([localpath, logfolder])

            try:
                os.makedirs(path)
            except OSError, e:
                # If directory exists, continue to next folder
                if e.args[0] == 17:
                    continue
                raise e
