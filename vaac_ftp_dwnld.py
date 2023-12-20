# vaac_ftp_dwnld.py
# Aidan Gray
# 12/20/2023
# aidan.gray@idg.jhu.edu
#
# This script connects to the FTP server containing VAAC data, finds the most
# recent file, and saves it to the local machine.
###############################################################################
import ftplib


# Quick function to connect to the server and return 
# a pointer to the ftplib.FTP object
def connectFTPserver():
    hostname = "tgftp.nws.noaa.gov"
    username = "anonymous"
    password = "username@email.com"
    data_dir = "SL.us008001/DF.c5/DC.textf/DS.vaafv"

    ftp = ftplib.FTP(hostname, username, password)  # Connect to the FTP server
    ftp.encoding = "utf-8"  # Set text encoding
    ftp.cwd(data_dir)  # Move into the appropriate directory

    return ftp


# Callback for FTP.retrlines(), which strips the newline character 
# from each line. This function restores the newline character and 
# collects the file contents in the 'data' variable.
def collectLines(s):
    global data
    data += s + '\n'


ftp = connectFTPserver()  # Connect to the FTP server

# Collect a list of all the filenames, sorted by time
all_files = ftp.nlst("-t")[2:]  # skip the first two, which are not real files
latest_file = all_files[0]  # first item is the latest file

# Retrieve each line from the file and pass it to collectLines()
data = ""
ftp.retrlines("RETR " + latest_file, collectLines)

# Write the data out to a file with the same name
with open(latest_file, 'w') as f:
    f.write(data)

ftp.close()
