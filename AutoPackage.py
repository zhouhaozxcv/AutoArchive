# -*- coding:utf-8 -*-
#!/usr/bin/python
import sys, os, getopt, time, shutil
from subprocess import call
from ftplib import FTP
from biplist import *

# 获取当前文件所在目录
def get_current_file_dir():
    current = sys.path[0]   #当前文件所在的文件夹
    os.chdir(current)       #进入到当前目录
    ##call('ls',shell=True)   #
    print ("当前目录：%s \n" %current)
    return current



#下载、更新git
def updateProjectFromGit():
    if os.path.exists(projectPath):
        print ("** git update start **\n")
        os.chdir(projectPath)
        # os.system('git branch')
        os.system('git fetch')
        os.popen('git diff')
        os.popen('git merge')

    else:
        print ("** git clone start **\n")
        os.popen('git init')
        os.popen('git clone git@git.***.com:iOS/***.git')
        # os.popen('git branch')



# 删除上一次打包的文件
def delIPA(path):
    if os.path.exists(path):
        filelist=[]  
        filelist=os.listdir(path)  
        for f in filelist:  
            filepath = os.path.join( path, f )  
            if os.path.isfile(filepath):  
                os.remove(filepath)  
                print filepath+" removed!"  
            elif os.path.isdir(filepath):  
                shutil.rmtree(filepath,True)  
                print "dir "+filepath+" removed!"
        os.rmdir(path)
    os.mkdir(ipaPath)
    os.chdir(ipaPath)

    

# 打包函数
def archive(CODE_SIGN_IDENTITY,PROVISIONING_PROFILE,ipaname,xcarchive_name, confi):
    os.system('xcodebuild -workspace %s/***.xcworkspace -scheme *** -configuration %s archive -archivePath %s CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s"' %(projectPath,confi,xcarchive_name,CODE_SIGN_IDENTITY,PROVISIONING_PROFILE))
    os.system('xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s/exportIPA.plist CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s"' %(xcarchive_name,ipaname,currentPath,CODE_SIGN_IDENTITY,PROVISIONING_PROFILE))
    ipa_path = "%s/%s" %(ipaPath,ipaname)
    os.chdir(ipa_path)
    os.system('mv ***.ipa %s' %ipaname)
    os.chdir(ipaPath)

    #获取xcarchive里面info.plist的版本号
    infoPath = "%s/%s/Info.plist" %(ipaPath, xcarchive_name)
    
    
    #获取xcarchive内部plist文件，以便获取版本号
    plist = readPlist(infoPath)


    #远程ftp目录
    remote_path = '***' + plist['ApplicationProperties']['CFBundleShortVersionString']
    UploadFilesToFTP(ipa_path, ipaname, remote_path)



#上传ftp
def UploadFilesToFTP(path,fileN,ftp_remote_path):

    ftp = FTP()
    ftp.set_debuglevel(2)
    timeout = 10000;
    port = 21;
    ftp.connect(ftp_server,port,timeout)
    ftp.login(ftp_user,ftp_password)
    # print ftp.getwelcome() #打印出欢迎信息
    ftp.cwd(ftp_remote_path)
    # list = ftp.nlst()       # 获得目录列表  
    # for name in list:
    #     print name

    filename = "%s/%s" %(path, fileN)
    print (filename)
    bufsize = 1024  #设置缓冲块大小
    fp = open(filename,'rb')
    upload = ftp.storbinary('STOR '+ fileN, fp, bufsize)
    ftp.set_debuglevel(0)  
    fp.close() #关闭文件  
    ftp.quit() 

    print ("\n%s --> ftp上传成功\n" %fileN)



currentPath = get_current_file_dir()                            #当前.py文件所在目录
projectPath = currentPath + '/***'                         #clone的工程文件所在目录
ipaPath = currentPath + '/ipa'                                  #打包文件所在目录

updateProjectFromGit()
delIPA(ipaPath)

#获取当前时间
timesec = time.time()
ftp_server='ftp.***.com'
ftp_user='ftp_username'
ftp_password='ftp_password'


# offline打包所需
CODE_SIGN_IDENTITY=""    #证书
PROVISIONING_PROFILE=""     #配置文件
xcarchive_name = "***.xcarchive" %time.strftime('%Y%m%d.%H%M%S', time.localtime(timesec))    #.xcarchive文件所在目录
ipa_name = "***.ipa" %time.strftime('%Y%m%d.%H%M%S', time.localtime(timesec))                #.ipa文件所在目录




archive(CODE_SIGN_IDENTITY,PROVISIONING_PROFILE,ipa_name,xcarchive_name,"Debug")



print ("\n**全部打包完成**\n")