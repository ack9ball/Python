import ftplib
from os import chdir, path


class FTP(object):

    def __init__(self):
        self._connection = ftplib.FTP()
        self._binary = True

    def set_transfer_mode(self, binary=True):
        """Set the file transfer mode"""
        self._binary = binary

    def connect(self, ftp_server="", ftp_user="anonymous", ftp_password="nobody@nowhere.com"):
        """Connect to the remote server"""
        self._connection.login(ftp_server, ftp_user, ftp_password)

    def remote_cd(self, remote_directory):
        """Change the current working director on the remote server"""
        if remote_directory is str and len(remote_directory) > 0:
            self._connection.cwd(remote_directory)

    def local_cd(self, local_directory):
        """Change the local working directory"""
        if local_directory is str and len(local_directory) > 0:
            chdir(local_directory)

    def get_directory(self, filter="*.*"):
        """Return a list of files on the remote server
        :param filter: file filter.  ie: *.txt
        :return: file list
        """
        files = []
        try:
            files = self._connection.
            files = self._connection.nlst()
        except ftplib.error_perm as resp:
            pass
        return files

    def get_file(self, remote_filename, local_filename=None):
        """Get a file from the remote server"""
        if local_filename is None:
            local_filename = path.basename(remote_filename)

        if self._binary:
            self._connection.retrbinary("RETR " + remote_filename, local_filename.write)
        else:
            # use a lambda to add newlines to the lines read from the server
            self._connection.retrlines("RETR " + remote_filename, lambda s, w=local_filename.write: w(s+"\n"))

    def put_file(self, local_filename, remote_filename=None):
        """Put a local file onto the remote server"""
        if remote_filename is None:
            remote_filename = path.basename(local_filename)

        if self._binary:
            self._connection.storbinary("STOR " + remote_filename, open(local_filename, "rb"), 1024)
        else:
            self._connection.storlines("STOR " + remote_filename, open(local_filename))

    def put_files(self, file_list=[]):
        """Put a list of local files onto the remote server"""
        for file_name in file_list:
            if file_name is tuple:
                remote_name = file_name[0]
                local_name = file_name[1]
            elif file_name is str:
                remote_name = file_name
                local_name = file_name

            with open(local_name, 'w') as file:
                self._connection.b(remote_name, file)

    def get_files(self, file_list=[]):
        """Get a list of files from the remote server"""
        for file_name in file_list:
            if file_name is tuple:
                remote_name = file_name[0]
                local_name = file_name[1]
            elif file_name is str:
                remote_name = file_name
                local_name = file_name
            if self._binary:
                self.get_binary_file(remote_name, local_name)
            else:
                self.get_text_file(remote_name, local_name)

