import sys
import os
import shutil
import time
from ftplib import FTP
import ftplib
import tqdm

my_dirs = []  # global
my_files = []  # global
curdir = ''  # global
location1 = sys.argv[1]
location2 = sys.argv[2]

def get_type_of_location(location):
    return location.split(":")[0]

def get_zip_folder(path):
    split = path.split("\\")
    folder = ""
    index = 0
    while index < len(split) - 1:
        folder += split[index] + "\\"
        index += 1
    folder += split[index]
    return folder[0:-4]
def prepare_zip_file(zip, folder_name):
    shutil.unpack_archive(zip,folder_name)
    print("ZIP FILE PREPARED")
def get_location_name(location):
    return (location.split(get_type_of_location(location))[1])[1:]

def checkIfRootDirsExist(rootDir1, rootDir2) :
    if (not os.path.exists(rootDir1) and not os.path.isdir(rootDir1)) :
        raise Exception(rootDir1 + " doesn't exist")
    if (not os.path.exists(rootDir2) and not os.path.isdir(rootDir2)) :
        raise Exception(rootDir2 + " doesn't exist")
def syncDirs(rootDir1, rootDir2):
    for root1, dirs1, files1 in os.walk(rootDir1):
        for relativePath1 in dirs1 :
            fullPath1 = os.path.join(root1, relativePath1)
            fullPath2 = fullPath1.replace(rootDir1, rootDir2)
            if os.path.exists(fullPath2) and os.path.isdir(fullPath2) :
                continue
            if os.path.exists(fullPath2) and os.path.isfile(fullPath2) :
                raise Exception("Cannot perform dir sync." + str(fullPath2) + " should be a dir, not a file!")
            # Case 1 : dest dir does not exit
            shutil.copytree(fullPath1, fullPath2)
            print("Directory " + str(fullPath2) + " copied from " + str(fullPath1))
            continue
    for root2, dirs2, files2 in os.walk(rootDir2):
        for relativePath2 in dirs2:
            fullPath2 = os.path.join(root2, relativePath2)
            fullPath1 = fullPath2.replace(rootDir2, rootDir1)
            if os.path.exists(fullPath1) and os.path.isdir(fullPath1) :
                continue
            if os.path.exists(fullPath1) and os.path.isfile(fullPath1) :
                raise Exception("Cannot perform dir sync." + str(fullPath1) + " should be a dir, not a file!")
            # Case 3 : dest dir exists but not src dir, so we need to copy it
            shutil.copytree(fullPath2, fullPath1)
            print("Directory " + str(fullPath1) + " copied from" + str(fullPath2))
            continue
def syncFiles(rootDir1, rootDir2):
    for root1, dirs1, files1 in os.walk(rootDir1):
        for file1 in files1:
            fullPath1 = os.path.join(root1, file1)
            fullPath2 = fullPath1.replace(rootDir1, rootDir2)
            # Case 1 : the file does not exist in dest dir
            if (not os.path.exists(fullPath2)) :
                shutil.copy2(fullPath1, fullPath2)
                print("File " + str(fullPath2) + " copied from " + str(fullPath1))
                continue
            # Case 2 : src file is more recent than dest file
            file1LastModificationTime = round(os.path.getmtime(fullPath1))
            file2LastModificationTime = round(os.path.getmtime(fullPath2))
            if (file1LastModificationTime > file2LastModificationTime):
                os.remove(fullPath2)
                shutil.copy2(fullPath1, fullPath2)
                print("File " + str(fullPath2) + " synchronized from " + str(fullPath1))
                continue
            # Case 3 : dest file is more recent than src file
            if (file1LastModificationTime < file2LastModificationTime):
                os.remove(fullPath1)
                shutil.copy2(fullPath2, fullPath1)
                print("File " + str(fullPath1) + " synchronized from " + str(fullPath2))
                continue
    # Case 4 : file only exists in dest dir but not in src
    # So, we copy it back to src dir
    for root2, dirs2, files2 in os.walk(rootDir2):
        for file2 in files2:
            fullPath2 = os.path.join(root2, file2);
            fullPath1 = fullPath2.replace(rootDir2, rootDir1);
            if (os.path.exists(fullPath1)):
                continue
            shutil.copy2(fullPath2, fullPath1)
            print("File " + str(fullPath1) + " copied from " + str(fullPath2))

def generate_list(path):
    list_for_path = []
    for root, dirs, files in os.walk(path):
        for name in files:
            list_for_path.append([os.path.join(root,name), os.path.getmtime(os.path.join(root,name))])
            list_for_path.append([os.path.join(root,name), os.path.getmtime(os.path.join(root, name))])
        for dir in dirs:
            list_for_path.append([os.path.join(root,dir), os.path.getmtime(os.path.join(root, dir))])
            list_for_path.append([os.path.join(root, dir), os.path.getmtime(os.path.join(root, dir))])
    return list_for_path

def delete_folders(rootDir1, rootDir2): #this function will delete all deleted folders from rootDir1 and changes will apply to rootDir2
    for root2, dirs2, files2 in os.walk(rootDir2):
        for relativePath2 in dirs2:
            fullPath2 = os.path.join(root2, relativePath2)
            fullPath1 = fullPath2.replace(rootDir2, rootDir1)
            if (not os.path.exists(fullPath1)) and os.path.isdir(fullPath1) :
                continue
            if os.path.exists(fullPath1) and os.path.isfile(fullPath1) :
                raise Exception("Cannot perform dir sync." + str(fullPath1) + " should be a dir, not a file!")
            # Case 3 : dest dir exists but not src dir, so we need to copy it
            shutil.rmtree(fullPath2)
            print("Directory " + str(fullPath2) + " deleted from" + str(rootDir2))
            continue

def delete_files(rootDir1, rootDir2, list_for_path1, list_for_path2): #this function will delete all files that are deleted from one path to another
    list_for_path1_second = generate_list(rootDir1)
    list_for_path2_second = generate_list(rootDir2)
    print(list_for_path1)
    print(list_for_path1_second)
    print(list_for_path2)
    print(list_for_path2_second)
    if len(list_for_path1_second) > len(list_for_path2_second):
        print("list1>list2")
        for file, time in list_for_path1:
            formed_file = file.replace(rootDir1, rootDir2)
            ok = 0
            for file1, time1 in list_for_path2:
                if formed_file == file1:
                    ok = 1
            if ok == 0:
                os.remove(file)
                print("File " + file + " deleted from " + rootDir1)
                break
    else:
        print("list2>list1")
        for file, time in list_for_path2:
            formed_file = file.replace(rootDir2, rootDir1)
            ok = 0
            for file1, time1 in list_for_path1:
                if formed_file == file1:
                    ok = 1
            if ok == 0:
                os.remove(file)
                print("File " + file + " deleted from " + rootDir2)
                break

def continue_sync_folders(folder1,folder2):
    list_for_path1 = generate_list(folder1)
    list_for_path2 = generate_list(folder2)
    time.sleep(1)
    list_for_path1_second = generate_list(folder1)
    list_for_path2_second = generate_list(folder2)
    print(list_for_path1)
    print(list_for_path1_second)
    print(list_for_path2)
    print(list_for_path2_second)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        print("needs sync")
        syncDirs(folder1, folder2)
        syncFiles(folder1, folder2)
    else:
        print("needs modification")
        delete_files(folder1, folder2,list_for_path1_second, list_for_path2_second)

def continue_sync_folder_and_zip(folder,zip_folder):
    list_for_path1 = generate_list(folder)
    list_for_path2 = generate_list(zip_folder)
    list_for_path1_second = generate_list(folder)
    list_for_path2_second = generate_list(zip_folder)
    print(list_for_path1)
    print(list_for_path1_second)
    time.sleep(2)
    print(list_for_path2)
    print(list_for_path2_second)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(
            list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        print("needs sync")
        syncDirs(folder, zip_folder)
        syncFiles(folder, zip_folder)
    else:
        print("needs modification")
        delete_files(folder, zip_folder, list_for_path1_second, list_for_path2_second)
    zip_file = zip_folder + ".zip"
    os.remove(zip_file)
    shutil.make_archive(zip_folder, "zip", zip_folder)

def continue_sync_zip_and_zip(folder1, folder2):
    list_for_path1 = generate_list(folder1)
    list_for_path2 = generate_list(folder2)
    time.sleep(2)  # waits 2 seconds to let the script run and get all the files okay
    list_for_path1_second = generate_list(folder1)
    list_for_path2_second = generate_list(folder2)
    print(list_for_path1)
    print(list_for_path1_second)
    time.sleep(2)
    print(list_for_path2)
    print(list_for_path2_second)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(
            list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        print("needs sync")
        syncDirs(folder1, folder2)
        syncFiles(folder1, folder2)
    else:
        print("needs modification")
        delete_files(folder1, folder2, list_for_path1_second, list_for_path2_second)
    zip_file1 = folder1 + ".zip"
    os.remove(zip_file1)
    shutil.make_archive(folder1, "zip", folder1)
    zip_file2 = folder2 + ".zip"
    os.remove(zip_file2)
    shutil.make_archive(folder2, "zip", folder2)

def initial_step(path1,path2):
    try:
        checkIfRootDirsExist(path1, path2)
        syncDirs(path1, path2)
        syncFiles(path1, path2)
    except Exception as e:
        print(e)
        print("End sync with failure!")
def sync_folders(path1,path2):
    print("Doing initial sync...")
    initial_step(path1,path2)
    print("First sync done, proceeding with sync of files")
    while 1:
        time.sleep(1)
        continue_sync_folders(path1,path2)

def sync_folder_and_zip(folder,zip_folder):
    print("Doing initial sync...")
    initial_step(folder,zip_folder)
    zip_file = zip_folder + ".zip"
    os.remove(zip_file)
    shutil.make_archive(zip_folder,"zip",zip_folder)
    print("First sync done, proceeding with sync of files")
    while 1:
        time.sleep(1)
        continue_sync_folder_and_zip(folder,zip_folder)

def sync_zip_and_zip(folder1, folder2):
    print("Doing initial sync...")
    initial_step(folder1, folder2)
    zip_file1 = folder1 + ".zip"
    zip_file2 = folder2 + ".zip"
    os.remove(zip_file1)
    os.remove(zip_file2)
    shutil.make_archive(folder1, "zip", folder1)
    shutil.make_archive(folder2, "zip", folder2)
    print("First sync done, proceeding with sync of files")
    while 1:
        time.sleep(1)
        continue_sync_zip_and_zip(folder1, folder2)

def traverse(ftp, depth=0):
    """
    return a recursive listing of an ftp server contents (starting
    from the current directory)

    listing is returned as a recursive dictionary, where each key
    contains a contents of the subdirectory or None if it corresponds
    to a file.

    @param ftp: ftplib.FTP object
    """
    if depth > 10:
        return ['depth > 10']
    level = {}
    for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
        try:
            ftp.cwd(entry)
            level[entry] = traverse(ftp, depth+1)
            ftp.cwd('..')
        except ftplib.error_perm:
            level[entry] = None
    return level


def get_dirs(ln):
    global my_dirs
    global my_files
    cols = ln.split(' ')
    objname = cols[len(cols) - 1]  # file or directory name
    if ln.startswith('d'):
        my_dirs.append(objname)
    else:
        if objname[-4] == ".":
            my_files.append(os.path.join(curdir, objname))  # full path


def check_dir(ftp, adir, dest_folder):
    global my_dirs
    global my_files  # let it accrue, then fetch them all later
    global curdir
    my_dirs = []
    gotdirs = []  # local
    curdir = ftp.pwd()
    print("going to change to directory " + adir + " from " + curdir)
    ftp.cwd(adir)
    curdir = ftp.pwd()
    path = os.path.join(dest_folder,curdir)
    print(path)
    print("now in directory: " + curdir)
    ftp.retrlines('LIST', get_dirs)
    gotdirs = my_dirs
    print("found in " + adir + " directories:")
    print(gotdirs)
    print("Total files found so far: " + str(len(my_files)) + ".")
    time.sleep(1)
    for subdir in gotdirs:
        my_dirs = []
        check_dir(ftp, subdir, dest_folder)  # recurse

    ftp.cwd('..')  # back up a directory when done here

def deletedir_ftp(ftp, dirname):
    ftp.cwd(dirname)
    print(dirname)
    for file in ftp.nlst():
        try:
            ftp.delete(file)
        except Exception:
            deletedir_ftp(ftp, file)
    ftp.cwd("..")
    ftp.rmd(dirname)

def remove_all_from_ftp(ftp, folder):
    ftp.cwd(folder)
    for ftpfile in ftp.nlst():
        try:
            ftp.delete(ftpfile)
        except Exception:
            deletedir_ftp(ftp, ftpfile)

def upload_all_to_ftp(ftp, path):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            print("STOR", name, localpath)
            ftp.storbinary('STOR ' + name, open(localpath,'rb'))
        elif os.path.isdir(localpath):
            print("MKD", name)

            try:
                ftp.mkd(name)

            # ignore "directory already exists"
            except ftplib.error_perm as e:
                if not e.args[0].startswith('550'):
                    raise

            print("CWD", name)
            ftp.cwd(name)
            upload_all_to_ftp(ftp, localpath)
            print("CWD", "..")
            ftp.cwd("..")


def rsync(location1, location2):
    type1 = get_type_of_location(location1)
    type2 = get_type_of_location(location2)
    name1 = get_location_name(location1)
    name2 = get_location_name(location2)
    if type1 == "folder" and type2 == "folder":
        print("Synchronizing folders " + name1 + " and " + name2)
        sync_folders(name1, name2)
    elif type1 == "folder" and type2 == "zip":
        zip = name2 + "zip"
        folder = get_zip_folder(zip)
        print(folder)
        prepare_zip_file(zip, folder)
        print("Synchronizing folder " + name1 + " and zip " + zip)
        sync_folder_and_zip(name1,folder)
    elif type1 == "zip" and type2 == "folder":
        zip = name1 + "zip"
        folder = get_zip_folder(zip)
        print(folder)
        prepare_zip_file(zip, folder)
        print("Synchronizing zip " + zip + " and folder " + name2)
        sync_folder_and_zip(name2, folder)
    elif type1 == "zip" and type2 == "zip":
        zip1 = name1 + "zip"
        folder1 = get_zip_folder(zip1)
        print(folder1)
        prepare_zip_file(zip1, folder1)
        zip2 = name2 + "zip"
        folder2 = get_zip_folder(zip2)
        print(folder2)
        prepare_zip_file(zip2, folder2)
        print("Synchronizing zip " + zip1 + " and zip " + zip2)
        sync_zip_and_zip(folder1, folder2)
    elif type1 == "ftp":
        print(name1)
        print(name2)
        username = name1.split(":")[0]
        password = name1.split(":")[1].split("@")[0]
        server = name1.split(":")[1].split("@")[1].split("/")[0]
        folder_name = name1.split("/")[1]
        print("username: " + username)
        print("password: " + password)
        print("server: " + server)
        print("folder name: " + folder_name)
        try:
            ftp = FTP(server)
            print(ftp.login(username, password))

            # ftp.retrlines('LIST')
            # ftp.quit()
            # parent_dir = ftp.pwd()
            # ftp.cwd('{}/{}'.format(parent_dir, folder_name))
            # files = ftp.nlst()
            # for f in files:
            #     print(f)
            check_dir(ftp, folder_name, "D:\\TESTFTP")  # directory to start in
            ftp.cwd('/.')  # change to root directory for downloading
            for f in my_files:
                print('getting ' + f)
                file_name = f.replace('/', '\\')  # use path as filename prefix, with underscores
                ftp.retrbinary('RETR ' + f, open("D:\\TESTFTP" + file_name, 'wb').write)
                time.sleep(1)
        except ftplib.error_perm as error:
            print(error)
    elif type2 == "ftp":
        print(name2)
        username = name2.split(":")[0]
        password = name2.split(":")[1].split("@")[0]
        server = name2.split(":")[1].split("@")[1].split("/")[0]
        folder_name = "/" + name2.split("/")[1]
        print("username: " + username)
        print("password: " + password)
        print("server: " + server)
        print("folder name: " + folder_name)
        try:
            ftp = FTP(server)
            print(ftp.login(username, password))
            ftp.retrlines('LIST')
            ftp.quit()
        except ftplib.error_perm as error:
            print(error)
    else:
        print("LOCATION TYPES UNAVAILABLE")

rsync(location1,location2)