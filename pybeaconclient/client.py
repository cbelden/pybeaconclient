import paramiko
import os


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

    def get_logs(self, devicepath, localpath):
        """Retrieves the beacon logs stored on the logging device at devicepath and stores them locally in localpath."""

        # Format directories
        devicepath = devicepath.rstrip('/')
        localpath = localpath.rstrip('/')

        # Get log directories (one for each day EXCEPT most recent)
        stdin, stdout, stderr = self._ssh.exec_command('ls ' + devicepath)
        logfolders = [d.rstrip() for d in stdout.readlines()[:-1]]

        # Print no. found folders
        print 'Found ', len(logfolders), ' to retrieve..'

        # Create local log folders
        self._create_log_folders(localpath, logfolders)

        # Open sftp session
        ftp = self._ssh.open_sftp()

        # Copy beacon logs to local machine
        for logfolder in logfolders:

            fullpath = '/'.join([devicepath, logfolder])
            stdin, stdout, stderr = self._ssh.exec_command('ls ' + fullpath)
            logs = [l.rstrip() for l in stdout.readlines()]

            print 'Copying ' + logfolder + ' ...'

            for log in logs:

                src = '/'.join([devicepath, logfolder, log])
                target = '/'.join([localpath, logfolder, log])

                print '\tfetching ' + log + '...'

                try:
                    ftp.get(src, target)
                except Exception:
                    print '*** Error copying ' + src + ' to ' + target

        ftp.close()

    def _create_log_folders(self, localpath, logfolders):
        """Generates a local log directory in localpath for each directory in logfolders."""

        for logfolder in logfolders:

            path = '/'.join([localpath, logfolder])

            try:
                os.makedirs(path)

            except OSError:
                print 'Error creating directory: ' + path
