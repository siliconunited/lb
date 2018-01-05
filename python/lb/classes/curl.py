import os
import stat
import argparse
import sys
import pycurl
import time
import random
import progressbar
import click

"""
classes/curl.py
Handles downloading files from the internet
Source: https://bitbucket.org/petebunting/rsgis_scripts/src/9110eb6ec2cec06595f55bb581c165adcaf6ebcf/Download/CURLDownloadFileList.py?at=default&fileviewer=file-view-default
"""

class CURLDownloadFileList(object):

    def __init__(self):
        pass

    def start(self, downloadDict, logPath='logs', logFile='error.log'):
        log_file = os.path.abspath(os.path.join(logPath, logFile))
        self._downloadFiles(downloadDict, log_file)

    def _readFileList(self, fileList):
        fTxt = open(fileList, 'r')
        files = []
        for line in fTxt:
            line = line.strip()
            if (not len(line) == 0) and (not line[0] == '#'):
                files.append(line)
        return files

    def _downloadProgress(self, download_t, download_d, upload_t, upload_d):
        # if download_d == 0.0:
        #     self.bar.start()

        if download_d < self.maxval:
            self.bar.update(int(download_d))

    def _downloadFiles(self, fileList, failsListFile, pauseTimeInit=0, fileCheck=False, timeOut=28800):

        # if fileListFile is not None:
        #     print(fileListFile)
        #     fileList = self._readFileList(fileListFile)
        #     print(fileList)

        # click.echo(fileList);

        # Create the fails list with blank file.
        failsFile = open(failsListFile, 'w')
        failsFile.close()

        halfPause = int(pauseTimeInit/2)
        lowPauseTime = pauseTimeInit - halfPause
        upPauseTime = pauseTimeInit + halfPause

        for benchmark in fileList:
            for file in fileList[benchmark]:
                url = file['url']
                path = file['path']
                content_length = int(file['filesize'])
                fileName = url.split('/')[-1]
                downloadFile = True
                if fileCheck:
                    if os.path.exists(os.path.join(path, fileName)):
                        downloadFile = False
                    else:
                        downloadFile = True

                if downloadFile:
                    fp = open(os.path.join(path, fileName), "wb")
                    self.curl = pycurl.Curl()
                    self.curl.setopt(pycurl.NOPROGRESS, 0)
                    self.curl.setopt(pycurl.PROGRESSFUNCTION, self._downloadProgress)
                    self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
                    self.curl.setopt(pycurl.MAXREDIRS, 5)
                    self.curl.setopt(pycurl.CONNECTTIMEOUT, 50)
                    self.curl.setopt(pycurl.FTP_RESPONSE_TIMEOUT, 600)
                    self.curl.setopt(pycurl.NOSIGNAL, 1)
                    self.maxval = int(content_length)
                    self.curl.setopt(pycurl.URL, url)
                    self.curl.setopt(pycurl.WRITEDATA, fp)

                    try:
                        click.echo("Start time: " + time.strftime("%c"))

                        # Setup the progress bar
                        content_length_in_kb = content_length / 1024
                        self.bar = progressbar.ProgressBar(
                                maxval = int(content_length),
                                widgets = [
                                    fileName, ' ',
                                    progressbar.Bar(),
                                    ' ', progressbar.Percentage()
                                    ]
                            ).start()
                        # Start the download
                        self.curl.perform()
                        self.bar.finish()
                        click.echo("\nTotal-time: " + str(self.curl.getinfo(self.curl.TOTAL_TIME)))
                        download_speed = self.curl.getinfo(self.curl.SPEED_DOWNLOAD)
                        click.echo("Download speed: %.2f bytes/second" % download_speed)
                        doc_size = self.curl.getinfo(self.curl.SIZE_DOWNLOAD)
                        # doc_size = self.curl.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
                        click.echo("Document size: %d bytes" % doc_size)
                    except:
                        failsFile = open(failsListFile, 'a')
                        failsFile.write(url + "\n")
                        failsFile.close()
                        import traceback
                        traceback.print_exc(file=sys.stderr)
                        sys.stderr.flush()
                self.curl.close()
                fp.close()
                # Change the permissions just to make sure it's executable
                # st = os.stat(os.path.join(path, fileName))
                # click.echo(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                # os.chmod(os.path.join(path, fileName), st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

                sys.stdout.flush()
                # Pause in loop - give the server time before another connection is made...
                pauseTime = random.randint(lowPauseTime, upPauseTime)
                click.echo("Pausing for " + str(pauseTime) + " seconds.\n")
                time.sleep(pauseTime)
