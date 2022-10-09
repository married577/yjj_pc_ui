import os
import sys
import ftplib
from common.fileReader import IniUtil
from config.file_path import REPORT_PATH, TEST_CASE_PATH


server_ip = IniUtil().get_value_of_option('ftp', 'server_ip')
ftp_username = IniUtil().get_value_of_option('ftp', 'ftp_username')
ftp_password = IniUtil().get_value_of_option('ftp', 'ftp_password')
LocalFile_test = IniUtil().get_value_of_option('ftp', 'LocalFile_test')
RemoteFile_test = IniUtil().get_value_of_option('ftp', 'RemoteFile_test')
LocalFile_pre = IniUtil().get_value_of_option('ftp', 'LocalFile_pre')
RemoteFile_pre = IniUtil().get_value_of_option('ftp', 'RemoteFile_pre')
LocalFile_prod = IniUtil().get_value_of_option('ftp', 'LocalFile_prod')
RemoteFile_prod = IniUtil().get_value_of_option('ftp', 'RemoteFile_prod')

class Ftp_result:
    ftp = ftplib.FTP()

    def __init__(self, host, port=2121):
        self.ftp.connect(host, port)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载当个文件
        file_handler = open(LocalFile, 'wb')
        self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)  # 接收服务器上文件并写入本地文件
        file_handler.close()
        return True

    def UpLoadFile(self, LocalFile, RemoteFile):
        if os.path.isfile(LocalFile) == False:
            return False
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary('STOR %s' % RemoteFile, file_handler, 4096)  # 上传文件
        file_handler.close()
        return True


    def show(self, list):
        result = list.lower().split(" ")
        if self.path in result and "<dir>" in result:
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.quit()

if __name__ == "__main__":
    ftp = Ftp_result(server_ip)
    ftp.Login(ftp_username, ftp_password)  # 登录，如果匿名登录则用空串代替即可
    # ftp.DownLoadFileTree('E:/study', '/owt/20170504')  # 从目标目录下载到本地目录E盘
    # ftp.UpLoadFileTree('E:/study', '/owt/20170504')
    # ftp.DownLoadFile('E:/study/r2101-ROOT-20170428.zip','/owt/20170504/r2101-ROOT-20170428.zip')
    # ftp.UpLoadFile(LocalFile_pre + '201901141554_result.html', RemoteFile_pre + '201901141554_result.html')
    print(REPORT_PATH + '\\' + '1212.html', RemoteFile_pre + '2121.html')
    ftp.UpLoadFile(REPORT_PATH + '\\' + '1212.html', RemoteFile_pre + '2121.html')

    ftp.close()
    print("上传数据成功")
