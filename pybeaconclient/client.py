import paramiko
import os


class PyBeaconClient():
    """Communicates with a pybeacon device."""

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
        """Retrieves the beacon logs stored on the logging device and stores them in localpath."""

        # Get log directories (one for each day EXCEPT most recent)
        stdin, stdout, stderr = self._ssh.exec_command('ls ' + devicepath)
        # logfolders = [d.rstrip() for d in stdout.readlines()[:-1]]
        logfolders = [d.rstrip() for d in stdout.readlines()]

        # Create local log folders
        self._create_log_folders(localpath, logfolders)

        # Open sftp session
        ftp = self._ssh.open_sftp()

        # Copy beacon logs to local machine
        for logfolder in logfolders:

            fullpath = '/'.join([devicepath, logfolder])
            stdin, stdout, stderr = self._ssh.exec_command('ls ' + fullpath)
            logs = [l.rstrip() for l in stdout.readlines()]

            for log in logs:

                src = '/'.join([devicepath, logfolder, log])
                target = '/'.join([localpath, logfolder, log])

                try:
                    ftp.get(src, target)
                except Exception:
                    print 'Error copying ' + src + ' to ' + target

        ftp.close()

    def _create_log_folders(self, localpath, logfolders):
        """Generates a directory for each listin gin logfolders in the directory specified by localpath."""

        for logfolder in logfolders:

            path = '/'.join([localpath, logfolder])

            try:
                os.makedirs(path)

            except OSError:
                print 'Error creating directory: ' + path
