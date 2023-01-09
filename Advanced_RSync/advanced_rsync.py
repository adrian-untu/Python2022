import logging
import sys
import os
import shutil
import time
from ftplib import FTP
import ftplib
from datetime import datetime

# First, we will create the log file in which we will provide logging
now = datetime.now()
current_time = now.strftime("%d-%m-%Y_%H-%M-%S")
logging.basicConfig(filename="logs" + current_time + ".log", level=logging.INFO)

# Second, we will declare global variables, used later on in the algorithm
# (without location1 and location2 which take argv values we cannot continue)
my_dirs = []
my_files = []
curdir = ''
location1 = sys.argv[1]
location2 = sys.argv[2]

def get_type_of_location(location):
    """
    This function will get the type of the location: zip, folder, ftp
    @params: location -> value provided as sys.argv value
    """
    return location.split(":")[0]

def get_zip_folder(path):
    """
    This function will get the name of the zip folder
    @params: path -> localization of zip to be able to create a folder
    """
    split = path.split("\\")
    folder = ""
    index = 0
    while index < len(split) - 1:
        folder += split[index] + "\\"
        index += 1
    folder += split[index]
    # We will return the name without the .zip part
    return folder[0:-4]

def prepare_zip_file(zip, folder_name):
    """
    This function will unpack the zip file to a certain destination
    @params: zip -> path of zip file
             folder_name -> path of destination folder
    """
    shutil.unpack_archive(zip,folder_name)
    print("ZIP FILE PREPARED")
    logging.info("ZIP FILE PREPARED")

def get_location_name(location):
    """
    This function will return the name of the location that we will have to take into consideration
    @params: location -> provided as sys.argv value
    """
    return (location.split(get_type_of_location(location))[1])[1:]

def checkIfRootDirsExist(rootDir1, rootDir2) :
    """
    This function will check if the two folders actually exist (useful for sync) and are directories
    @params: rootDir1, rootDir2 -> paths that we will check if they exist and if they are directories
    """
    if (not os.path.exists(rootDir1) and not os.path.isdir(rootDir1)) :
        logging.error(rootDir1 + " doesn't exist")
        raise Exception(rootDir1 + " doesn't exist")
    if (not os.path.exists(rootDir2) and not os.path.isdir(rootDir2)) :
        logging.error(rootDir2 + " doesn't exist")
        raise Exception(rootDir2 + " doesn't exist")
def syncDirs(rootDir1, rootDir2):
    """
    This function will be taking care of the sync of directories, in such ways that:
    => if a folder is created on one side, it will also be created on the other side
    @params: rootDir1, rootDir2 -> paths for which we will sync the directories
    !It is necessary to do this before file sync because of permission issues with paths in folders that do not exist!
    """
    for root1, dirs1, files1 in os.walk(rootDir1):
        for relativePath1 in dirs1:
            fullPath1 = os.path.join(root1, relativePath1)
            fullPath2 = fullPath1.replace(rootDir1, rootDir2)
            if os.path.exists(fullPath2) and os.path.isdir(fullPath2):
                continue
            if os.path.exists(fullPath2) and os.path.isfile(fullPath2):
                logging.error("Cannot perform dir sync." + str(fullPath2) + " should be a dir, not a file!")
                raise Exception("Cannot perform dir sync." + str(fullPath2) + " should be a dir, not a file!")
            # Case 1 : destination directory does not exit
            shutil.copytree(fullPath1, fullPath2)
            logging.info("Directory " + str(fullPath2) + " copied from " + str(fullPath1))
            print("Directory " + str(fullPath2) + " copied from " + str(fullPath1))
            continue
    for root2, dirs2, files2 in os.walk(rootDir2):
        for relativePath2 in dirs2:
            fullPath2 = os.path.join(root2, relativePath2)
            fullPath1 = fullPath2.replace(rootDir2, rootDir1)
            if os.path.exists(fullPath1) and os.path.isdir(fullPath1) :
                continue
            if os.path.exists(fullPath1) and os.path.isfile(fullPath1) :
                logging.error("Cannot perform dir sync." + str(fullPath1) + " should be a dir, not a file!")
                raise Exception("Cannot perform dir sync." + str(fullPath1) + " should be a dir, not a file!")
            # Case 2 : destination directory exists but not source directory, so we need to copy it
            shutil.copytree(fullPath2, fullPath1)
            logging.info("Directory " + str(fullPath1) + " copied from" + str(fullPath2))
            print("Directory " + str(fullPath1) + " copied from" + str(fullPath2))
            continue

def syncFiles(rootDir1, rootDir2):
    """
    This function will be taking care of the sync of files, in such ways that:
    => if a file is deleted on one side, it will also be deleted on the other side
    => if a file is created on one side, it will also be created on the other side
    => if a file is modified on one side, it will also be modified on the other side
    @params: rootDir1, rootDir2 -> paths for which we will sync the files
    """
    for root1, dirs1, files1 in os.walk(rootDir1):
        for file1 in files1:
            fullPath1 = os.path.join(root1, file1)
            fullPath2 = fullPath1.replace(rootDir1, rootDir2)
            # Case 1 : the file does not exist in destination directory
            if (not os.path.exists(fullPath2)) :
                shutil.copy2(fullPath1, fullPath2)
                logging.info("File " + str(fullPath2) + " copied from " + str(fullPath1))
                print("File " + str(fullPath2) + " copied from " + str(fullPath1))
                continue
            # Case 2 : source file is more recent than destination file
            file1LastModificationTime = round(os.path.getmtime(fullPath1))
            file2LastModificationTime = round(os.path.getmtime(fullPath2))
            if (file1LastModificationTime > file2LastModificationTime):
                os.remove(fullPath2)
                shutil.copy2(fullPath1, fullPath2)
                logging.info("File " + str(fullPath2) + " synchronized from " + str(fullPath1))
                print("File " + str(fullPath2) + " synchronized from " + str(fullPath1))
                continue
            # Case 3 : destination file is more recent than source file
            if (file1LastModificationTime < file2LastModificationTime):
                os.remove(fullPath1)
                shutil.copy2(fullPath2, fullPath1)
                logging.info("File " + str(fullPath1) + " synchronized from " + str(fullPath2))
                print("File " + str(fullPath1) + " synchronized from " + str(fullPath2))
                continue
    # Case 4 : file only exists in destination directory but not in source directory. So, we copy it back to source directory
    for root2, dirs2, files2 in os.walk(rootDir2):
        for file2 in files2:
            fullPath2 = os.path.join(root2, file2)
            fullPath1 = fullPath2.replace(rootDir2, rootDir1)
            if (os.path.exists(fullPath1)):
                continue
            shutil.copy2(fullPath2, fullPath1)
            logging.info("File " + str(fullPath1) + " copied from " + str(fullPath2))
            print("File " + str(fullPath1) + " copied from " + str(fullPath2))

def generate_list(path):
    """
    This function will generate lists of paths for the next functions to validate as only requirement for the two functions above to take place
    @params: path -> path for which we will generate the list
    """
    list_for_path = []
    for root, dirs, files in os.walk(path):
        for name in files:
            list_for_path.append([os.path.join(root,name), os.path.getmtime(os.path.join(root,name))])
            list_for_path.append([os.path.join(root,name), os.path.getmtime(os.path.join(root, name))])
        for dir in dirs:
            list_for_path.append([os.path.join(root,dir), os.path.getmtime(os.path.join(root, dir))])
            list_for_path.append([os.path.join(root, dir), os.path.getmtime(os.path.join(root, dir))])
    # This list will contain elements which are in the following structure:
    # [[filename, timestamp],[filename1,timestamp1] etc.]
    return list_for_path

def delete_folders(rootDir1, rootDir2): #this function will delete all deleted folders from rootDir1 and changes will apply to rootDir2
    """
    This function will delete whole folders if they are deleted from any side
    @params: rootDir1, rootDir2 -> paths for which we will do this step of sync
    """
    for root2, dirs2, files2 in os.walk(rootDir2):
        for relativePath2 in dirs2:
            fullPath2 = os.path.join(root2, relativePath2)
            fullPath1 = fullPath2.replace(rootDir2, rootDir1)
            if (not os.path.exists(fullPath1)) and os.path.isdir(fullPath1):
                continue
            if os.path.exists(fullPath1) and os.path.isfile(fullPath1):
                logging.error("Cannot perform dir sync." + str(fullPath1) + " should be a dir, not a file!")
                raise Exception("Cannot perform dir sync." + str(fullPath1) + " should be a dir, not a file!")
            shutil.rmtree(fullPath2)
            logging.info("Directory " + str(fullPath2) + " deleted from" + str(rootDir2))
            print("Directory " + str(fullPath2) + " deleted from" + str(rootDir2))
            continue

def delete_files(rootDir1, rootDir2, list_for_path1, list_for_path2):
    """
        This function will delete files if they are deleted from any side
        @params: rootDir1, rootDir2 -> paths for which we will do this step of sync
                 list_for_path1, list_for_path2 -> lists provided by function generate_list(path)
        """
    list_for_path1_second = generate_list(rootDir1)
    list_for_path2_second = generate_list(rootDir2)
    if len(list_for_path1_second) > len(list_for_path2_second):
        for file, time in list_for_path1:
            formed_file = file.replace(rootDir1, rootDir2)
            ok = 0
            for file1, time1 in list_for_path2:
                if formed_file == file1:
                    ok = 1
            if ok == 0:
                os.remove(file)
                logging.info("File " + file + " deleted from " + rootDir1)
                print("File " + file + " deleted from " + rootDir1)
                break
    else:
        for file, time in list_for_path2:
            formed_file = file.replace(rootDir2, rootDir1)
            ok = 0
            for file1, time1 in list_for_path1:
                if formed_file == file1:
                    ok = 1
            if ok == 0:
                os.remove(file)
                logging.info("File " + file + " deleted from " + rootDir2)
                print("File " + file + " deleted from " + rootDir2)
                break

def get_dirs(ln):
    """
    This function is a step in the ftp sync, it will provide the directories from a current working directory
    @params: ln -> line for which we will get the names of the folders
    (the whole structure is in a table form in the ftp type)
    """
    global my_dirs
    global my_files
    cols = ln.split(' ')
    objname = cols[len(cols) - 1]
    if ln.startswith('d'):
        my_dirs.append(objname)
    else:
        if objname[-4] == ".":
            my_files.append(os.path.join(curdir, objname))

def check_dir(ftp, adir, dest_folder):
    """
    This function will create the directoey required in the local storage, before handling the files
    @params: ftp -> ftp type object which represents the server
             adir -> a directory name
             dest_folder -> path in which the directory will be created
    """
    global my_dirs
    global my_files
    global curdir
    my_dirs = []
    curdir = ftp.pwd()
    ftp.cwd(adir)
    curdir = ftp.pwd()
    path = os.path.join(dest_folder,curdir)
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)
    ftp.retrlines('LIST', get_dirs)
    gotdirs = my_dirs
    time.sleep(1)
    for subdir in gotdirs:
        my_dirs = []
        check_dir(ftp, subdir, dest_folder)
    ftp.cwd('..')

def remove_all_from_ftp(ftp, folder_name_ftp):
    """
    This function will remove all the files and folders from a ftp current working directory
    (including the directory itself)
    @params: ftp -> ftp type object which represents the server
             folder_name_ftp -> name of the folder in the server for which we are handling the contens
    """
    for (name, properties) in ftp.mlsd(path=folder_name_ftp):
        if name in ['.', '..']:
            continue
        elif properties['type'] == 'file':
            ftp.delete(f"{folder_name_ftp}/{name}")
        elif properties['type'] == 'dir':
            remove_all_from_ftp(ftp, f"{folder_name_ftp}/{name}")
    ftp.rmd(folder_name_ftp)

def upload_all_to_ftp(ftp, path):
    """
    This step will upload on the server the new version of the current working directory
    (it is an inefficient approach as it can be optimised to remove only one directory/file at once)
    (I did not have enough time for the efficiency)
    @params: -> ftp -> ftp type object which represents the server
                path -> folder from which we will upload all contents to the server
    """
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            ftp.storbinary('STOR ' + name, open(localpath,'rb'))
        elif os.path.isdir(localpath):
            try:
                ftp.mkd(name)
            except ftplib.error_perm as e:
                if not e.args[0].startswith('550'):
                    raise
            ftp.cwd(name)
            upload_all_to_ftp(ftp, localpath)
            ftp.cwd("..")

def initial_step(path1,path2):
    """
    This function will be the initial step for the project, as it will do the following actions:
    1. If a file or a folder is only in a location, it will be created also in the other one
    (the folder will also be uploaded with its contents)
    2. If the same file exists in both locations, but there are differences, the newest version will
    be available on both location.
    @params: path1, path2 -> folder paths for which we will do this step
        (it does not matter if the files are folders of zips or ftp, it is all the same as there are folders created)
    """
    try:
        checkIfRootDirsExist(path1, path2)
        syncDirs(path1, path2)
        syncFiles(path1, path2)
    except Exception as e:
        print(e)
        logging.error(e)
        logging.error("End sync with failure!")
        print("End sync with failure!")

def sync_folders(path1,path2):
    """
    This function will sync the folders and will proceed with the continuous sync
    in function continue_sync_folders(path1,path2)
    @params: path1, path2 -> folder paths for which we will do this step
        (this function is specific to sync of folders)
    """
    logging.info("Doing initial sync...")
    print("Doing initial sync...")
    initial_step(path1,path2)
    logging.info("First sync done, proceeding with the continuous sync")
    print("First sync done, proceeding with the continuous sync")
    while 1:
        time.sleep(1)
        continue_sync_folders(path1,path2)

def continue_sync_folders(folder1,folder2):
    """
    This function will do the continuous sync of the folders with the following requirements:
    1. If a file or a folder is only in a location, it will be created also in the other one
    (the folder will also be uploaded with its contents)
    2. If the same file exists in both locations, but there are differences, the newest version will
    be available on both location.
    3. If a file or a folder is deleted from a location, it will be deleted from both locations
    @params: folder1, folder2 -> folder paths
    """
    list_for_path1 = generate_list(folder1)
    list_for_path2 = generate_list(folder2)
    time.sleep(1)
    list_for_path1_second = generate_list(folder1)
    list_for_path2_second = generate_list(folder2)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        syncDirs(folder1, folder2)
        syncFiles(folder1, folder2)
    else:
        delete_files(folder1, folder2,list_for_path1_second, list_for_path2_second)

def sync_folder_and_zip(folder,zip_folder):
    """
    This function will sync a folder and a zip and will proceed with the continuous sync
    in function continue_sync_folder_and_zip(folder,zip_folder)
    @params: folder, zip_folder -> folder paths for which we will do this step
        (this function is specific to sync of a folder and a zip file)
    """
    logging.info("Doing initial sync...")
    print("Doing initial sync...")
    initial_step(folder,zip_folder)
    zip_file = zip_folder + ".zip"
    os.remove(zip_file)
    shutil.make_archive(zip_folder,"zip",zip_folder)
    logging.info("First sync done, proceeding with the continuous sync")
    print("First sync done, proceeding with the continuous sync")
    while 1:
        time.sleep(1)
        continue_sync_folder_and_zip(folder,zip_folder)

def continue_sync_folder_and_zip(folder,zip_folder):
    """
    This function will do the continuous sync of a folder and a zip file with the following requirements:
    1. If a file or a folder is only in a location, it will be created also in the other one
    (the folder will also be uploaded with its contents)
    2. If the same file exists in both locations, but there are differences, the newest version will
    be available on both location.
    3. If a file or a folder is deleted from a location, it will be deleted from both locations
    @params: folder,zip_folder -> folder paths
    When all steps are done, the zip archive will be reconstructed with
    function shutil.make_archive(zip_folder, "zip", zip_folder)
    """
    list_for_path1 = generate_list(folder)
    list_for_path2 = generate_list(zip_folder)
    list_for_path1_second = generate_list(folder)
    list_for_path2_second = generate_list(zip_folder)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(
            list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        syncDirs(folder, zip_folder)
        syncFiles(folder, zip_folder)
    else:
        delete_files(folder, zip_folder, list_for_path1_second, list_for_path2_second)
    zip_file = zip_folder + ".zip"
    os.remove(zip_file)
    shutil.make_archive(zip_folder, "zip", zip_folder)

def sync_zip_and_zip(folder1, folder2):
    """
    This function will sync two zip files and will proceed with the continuous sync
    in function continue_sync_zip_and_zip(folder1, folder2)
    @params: folder1, folder2 -> folder paths for which we will do this step
        (this function is specific to sync of zip files)
    """
    logging.info("Doing initial sync...")
    print("Doing initial sync...")
    initial_step(folder1, folder2)
    zip_file1 = folder1 + ".zip"
    zip_file2 = folder2 + ".zip"
    os.remove(zip_file1)
    os.remove(zip_file2)
    shutil.make_archive(folder1, "zip", folder1)
    shutil.make_archive(folder2, "zip", folder2)
    logging.info("First sync done, proceeding with the continuous sync")
    print("First sync done, proceeding with the continuous sync")
    while 1:
        time.sleep(1)
        continue_sync_zip_and_zip(folder1, folder2)

def continue_sync_zip_and_zip(folder1, folder2):
    """
    This function will do the continuous sync of zip files with the following requirements:
    1. If a file or a folder is only in a location, it will be created also in the other one
    (the folder will also be uploaded with its contents)
    2. If the same file exists in both locations, but there are differences, the newest version will
    be available on both location.
    3. If a file or a folder is deleted from a location, it will be deleted from both locations
    @params: folder,zip_folder -> folder paths
    When all steps are done, the zip archives will be reconstructed with
    function shutil.make_archive(zip_folder, "zip", zip_folder)
    """
    list_for_path1 = generate_list(folder1)
    list_for_path2 = generate_list(folder2)
    time.sleep(2)
    list_for_path1_second = generate_list(folder1)
    list_for_path2_second = generate_list(folder2)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(
            list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        syncDirs(folder1, folder2)
        syncFiles(folder1, folder2)
    else:
        delete_files(folder1, folder2, list_for_path1_second, list_for_path2_second)
    zip_file1 = folder1 + ".zip"
    os.remove(zip_file1)
    shutil.make_archive(folder1, "zip", folder1)
    zip_file2 = folder2 + ".zip"
    os.remove(zip_file2)
    shutil.make_archive(folder2, "zip", folder2)

def sync_folder_and_ftp(ftp,ftp_folder_name,ftp_local_path,folder_path):
    """
    This function will sync a folder and a ftp location and will proceed with the continuous sync
    in function continue_sync_folder_and_ftp(ftp,ftp_folder_name,ftp_local_path,folder_path)
    @params: ftp -> ftp type object which represents the server
             ftp_folder_name -> name of ftp location
             ftp_local_path -> location of downloaded files from server
             folder_path -> folder location
        (this function is specific to sync of folder and ftp location)
    """
    logging.info("Doing initial sync...")
    print("Doing initial sync...")
    initial_step(ftp_local_path,folder_path)
    logging.info("First sync done, proceeding with the continuous sync")
    print("First sync done, proceeding with the continuous sync")
    while 1:
        time.sleep(1)
        continue_sync_folder_and_ftp(ftp,ftp_folder_name,ftp_local_path,folder_path)

def continue_sync_folder_and_ftp(ftp, ftp_folder_name, ftp_local_path, folder_path):
    """
    This function will do the continuous sync of a folder and a ftp location with the following requirements:
    1. If a file or a folder is only in a location, it will be created also in the other one
    (the folder will also be uploaded with its contents)
    2. If the same file exists in both locations, but there are differences, the newest version will
    be available on both location.
    3. If a file or a folder is deleted from a location, it will be deleted from both locations
    @params: ftp -> ftp type object which represents the server
             ftp_folder_name -> name of ftp location
             ftp_local_path -> location of downloaded files from server
             folder_path -> folder location
    When all steps are done, the ftp location will be refreshed with the new content, using the functions
    remove_all_from_ftp(ftp,ftp_folder_name) and upload_all_to_ftp(ftp,ftp_local_path)
    """
    list_for_path1 = generate_list(ftp_local_path)
    list_for_path2 = generate_list(folder_path)
    list_for_path1_second = generate_list(ftp_local_path)
    list_for_path2_second = generate_list(folder_path)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(
            list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        syncDirs(ftp_local_path, folder_path)
        syncFiles(ftp_local_path, folder_path)
    else:
        delete_files(ftp_local_path, folder_path, list_for_path1_second, list_for_path2_second)
    logging.info("DELETING ALL FROM FTP...")
    print("DELETING ALL FROM FTP...")
    remove_all_from_ftp(ftp,ftp_folder_name)
    logging.info("UPLOADING ALL TO FTP...")
    print("UPLOADING ALL TO FTP...")
    ftp.mkd(ftp_folder_name)
    ftp.cwd(ftp_folder_name)
    upload_all_to_ftp(ftp,ftp_local_path)
    ftp.cwd("..")
    logging.info("DONE")
    print("DONE")

def sync_ftp_and_zip(ftp,ftp_folder_name,ftp_local_path,zip_folder):
    """
    This function will sync a zip file and a ftp location and will proceed with the continuous sync
    in function continue_sync_ftp_and_zip(ftp,ftp_folder_name,ftp_local_path,zip_folder)
    @params: ftp -> ftp type object which represents the server
             ftp_folder_name -> name of ftp location
             ftp_local_path -> location of downloaded files from server
             zip_folder -> zip folder location
        (this function is specific to sync of zip file and ftp location)
    """
    logging.info("Doing initial sync...")
    print("Doing initial sync...")
    initial_step(ftp_local_path,zip_folder)
    logging.info("First sync done, proceeding with the continuous sync")
    print("First sync done, proceeding with the continuous sync")
    while 1:
        time.sleep(1)
        continue_sync_ftp_and_zip(ftp,ftp_folder_name,ftp_local_path,zip_folder)

def continue_sync_ftp_and_zip(ftp,ftp_folder_name,ftp_local_path,zip_folder):
    """
    This function will do the continuous sync of a folder and a ftp location with the following requirements:
    1. If a file or a folder is only in a location, it will be created also in the other one
    (the folder will also be uploaded with its contents)
    2. If the same file exists in both locations, but there are differences, the newest version will
    be available on both location.
    3. If a file or a folder is deleted from a location, it will be deleted from both locations
    @params: ftp -> ftp type object which represents the server
             ftp_folder_name -> name of ftp location
             ftp_local_path -> location of downloaded files from server
             zip_folder -> zip folder location
    When all steps are done, the ftp location will be refreshed with the new content, using the functions
    remove_all_from_ftp(ftp,ftp_folder_name) and upload_all_to_ftp(ftp,ftp_local_path) AND
    The zip archive will be reconstructed with
    function shutil.make_archive(zip_folder, "zip", zip_folder)
    """
    list_for_path1 = generate_list(ftp_local_path)
    list_for_path2 = generate_list(zip_folder)
    time.sleep(2)
    list_for_path1_second = generate_list(ftp_local_path)
    list_for_path2_second = generate_list(zip_folder)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(
            list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        syncDirs(ftp_local_path, zip_folder)
        syncFiles(ftp_local_path, zip_folder)
    else:
        delete_files(ftp_local_path, zip_folder, list_for_path1_second, list_for_path2_second)
    zip_file1 = zip_folder + ".zip"
    os.remove(zip_file1)
    shutil.make_archive(zip_folder, "zip", zip_folder)
    logging.info("DELETING ALL FROM FTP...")
    print("DELETING ALL FROM FTP...")
    remove_all_from_ftp(ftp, ftp_folder_name)
    logging.info("UPLOADING ALL TO FTP...")
    print("UPLOADING ALL TO FTP...")
    ftp.mkd(ftp_folder_name)
    ftp.cwd(ftp_folder_name)
    upload_all_to_ftp(ftp, ftp_local_path)
    ftp.cwd("..")
    logging.info("DONE")
    print("DONE")

def sync_ftps(ftp,ftp_folder_name,ftp_local_path,ftp1,ftp_folder_name1,ftp_local_path1):
    """
    This function will sync two ftp locations and will proceed with the continuous sync
    in function continue_sync_ftps(ftp,ftp_folder_name,ftp_local_path,ftp1,ftp_folder_name1,ftp_local_path1)
    @params: ftp -> ftp type object which represents the server
             ftp_folder_name -> name of ftp location
             ftp_local_path -> location of downloaded files from server
             ftp1 -> ftp type object 2 which represents the server
             ftp_folder_name1 -> name of ftp location 2
             ftp_local_path1 -> location 2 of downloaded files from server
        (this function is specific to sync of ftp locations)
    """
    logging.info("Doing initial sync...")
    print("Doing initial sync...")
    initial_step(ftp_local_path,ftp_local_path1)
    logging.info("First sync done, proceeding with the continuous sync")
    print("First sync done, proceeding with the continuous sync")
    while 1:
        time.sleep(1)
        continue_sync_ftps(ftp,ftp_folder_name,ftp_local_path,ftp1,ftp_folder_name1,ftp_local_path1)

def continue_sync_ftps(ftp,ftp_folder_name,ftp_local_path,ftp1,ftp_folder_name1,ftp_local_path1):
    """
    This function will do the continuous sync of two ftp locations with the following requirements:
    1. If a file or a folder is only in a location, it will be created also in the other one
    (the folder will also be uploaded with its contents)
    2. If the same file exists in both locations, but there are differences, the newest version will
    be available on both location.
    3. If a file or a folder is deleted from a location, it will be deleted from both locations
    @params: ftp -> ftp type object which represents the server
             ftp_folder_name -> name of ftp location
             ftp_local_path -> location of downloaded files from server
             zip_folder -> zip folder location
    When all steps are done, the ftp locations will be refreshed with the new content, using the functions
    remove_all_from_ftp(ftp,ftp_folder_name) and upload_all_to_ftp(ftp,ftp_local_path)
    """
    list_for_path1 = generate_list(ftp_local_path)
    list_for_path2 = generate_list(ftp_local_path1)
    time.sleep(2)
    list_for_path1_second = generate_list(ftp_local_path)
    list_for_path2_second = generate_list(ftp_local_path1)
    if len(list_for_path1) == len(list_for_path2) and len(list_for_path1_second) == len(list_for_path2_second) or len(
            list_for_path1_second) > len(list_for_path1) or len(list_for_path2_second) > len(list_for_path2):
        syncDirs(ftp_local_path, ftp_local_path1)
        syncFiles(ftp_local_path, ftp_local_path1)
    else:
        delete_files(ftp_local_path, ftp_local_path1, list_for_path1_second, list_for_path2_second)
    logging.info("DELETING ALL FROM FTP...")
    print("DELETING ALL FROM FTP...")
    remove_all_from_ftp(ftp, ftp_folder_name)
    logging.info("UPLOADING ALL TO FTP...")
    print("UPLOADING ALL TO FTP...")
    ftp.mkd(ftp_folder_name)
    ftp.cwd(ftp_folder_name)
    upload_all_to_ftp(ftp, ftp_local_path)
    ftp.cwd("..")
    logging.info("DONE FOR FIRST FTP")
    print("DONE FOR FIRST FTP")
    logging.info("DELETING ALL FROM SECOND FTP...")
    print("DELETING ALL FROM SECOND FTP...")
    remove_all_from_ftp(ftp1, ftp_folder_name1)
    logging.info("UPLOADING ALL TO SECOND FTP...")
    print("UPLOADING ALL TO SECOND FTP...")
    ftp1.mkd(ftp_folder_name1)
    ftp1.cwd(ftp_folder_name1)
    upload_all_to_ftp(ftp1, ftp_local_path1)
    ftp1.cwd("..")
    logging.info("DONE FOR SECOND FTP")
    print("DONE FOR SECOND FTP")

def rsync(location1, location2):
    """
    This function is the brain of the project, the function that decides what types of locations they are AND
    what will be the approach with the locations
    @params: location1, location2 -> the locations provided to the script as sys.argv elements
    """
    type1 = get_type_of_location(location1)
    type2 = get_type_of_location(location2)
    name1 = get_location_name(location1)
    name2 = get_location_name(location2)
    if type1 == "folder" and type2 == "folder":
        # If the locations are folders, it is the easiest approach, we will sync directly
        logging.info("Synchronizing folders " + name1 + " and " + name2)
        print("Synchronizing folders " + name1 + " and " + name2)
        sync_folders(name1, name2)
    elif type1 == "folder" and type2 == "zip":
        # If the locations are a folder and a zip (in this order), we will need to prepare the location 2
        # (make a directory out of it) and then we will proceed with the sync
        zip = name2 + "zip"
        folder = get_zip_folder(zip)
        prepare_zip_file(zip, folder)
        logging.info("Synchronizing folder " + name1 + " and zip " + zip)
        print("Synchronizing folder " + name1 + " and zip " + zip)
        sync_folder_and_zip(name1,folder)
    elif type1 == "zip" and type2 == "folder":
        # If the locations are a zip and a folder (in this order), we will need to prepare the location 1
        # (make a directory out of it) and then we will proceed with the sync
        zip = name1 + "zip"
        folder = get_zip_folder(zip)
        prepare_zip_file(zip, folder)
        logging.info("Synchronizing zip " + zip + " and folder " + name2)
        print("Synchronizing zip " + zip + " and folder " + name2)
        sync_folder_and_zip(name2, folder)
    elif type1 == "zip" and type2 == "zip":
        # If the locations are two zip files, we will need to prepare the locations
        # (make directories out of them) and then we will proceed with the sync
        zip1 = name1 + "zip"
        folder1 = get_zip_folder(zip1)
        prepare_zip_file(zip1, folder1)
        zip2 = name2 + "zip"
        folder2 = get_zip_folder(zip2)
        prepare_zip_file(zip2, folder2)
        logging.info("Synchronizing zip " + zip1 + " and zip " + zip2)
        print("Synchronizing zip " + zip1 + " and zip " + zip2)
        sync_zip_and_zip(folder1, folder2)
    elif type1 == "ftp":
        # If the location 1 is a ftp location, first we will proceed to log in on the server, download all the files
        # and make a directory out of it, then we will proceed with the next steps
        username = name1.split(":")[0]
        password = name1.split(":")[1].split("@")[0]
        server = name1.split(":")[1].split("@")[1].split("/")[0]
        folder_name = name1.split("/")[1]
        try:
            ftp = FTP(server)
            ftp.login(username, password)
            check_dir(ftp, folder_name, "D:\\TESTFTP")
            ftp.cwd('/.')
            logging.info("Getting all files from ftp into a local path...")
            print("Getting all files from ftp into a local path...")
            # Value for my_files is obtained in function check_dir(ftp, folder_name, "D:\\TESTFTP")
            for f in my_files:
                file_name = f.replace('/', '\\')
                ftp.retrbinary('RETR ' + f, open("D:" + file_name, 'wb').write)
                time.sleep(1)
            logging.info("DONE")
            print("DONE")
            localpath = "D:\\" + folder_name
            if type2 == "folder":
                # If the second location is a folder, we will proceed directly with the sync
                logging.info("Synchronizing ftp " + name1 + " and folder " + name2)
                print("Synchronizing ftp " + name1 + " and folder " + name2)
                sync_folder_and_ftp(ftp,folder_name,localpath,name2)
            elif type2 == "zip":
                # If the second location is a zip file, we will first prepare it (unarchive and create a directory)
                # and then we will proceed with the sync
                zip = name2 + "zip"
                folder = get_zip_folder(zip)
                prepare_zip_file(zip, folder)
                logging.info("Synchronizing ftp " + name1 + " and zip " + folder)
                print("Synchronizing ftp " + name1 + " and zip " + folder)
                sync_ftp_and_zip(ftp,folder_name,localpath,folder)
            elif type2 == "ftp":
                # If the second location is a ftp location, we will proceed as in the first case,
                # then we will continue with the sync itself
                username1 = name2.split(":")[0]
                password1 = name2.split(":")[1].split("@")[0]
                server1 = name2.split(":")[1].split("@")[1].split("/")[0]
                folder_name1 = name2.split("/")[1]
                ftp1 = FTP(server1)
                ftp1.login(username1, password1)
                check_dir(ftp1, folder_name1, "D:")
                ftp1.cwd('/.')
                logging.info("Getting all files from ftp into a local path...")
                print("Getting all files from ftp into a local path...")
                # Value for my_files is obtained in function check_dir(ftp1, folder_name1, "D:\\TESTFTP")
                for f in my_files:
                    file_name = f.replace('/', '\\')
                    ftp.retrbinary('RETR ' + f, open("D:" + file_name, 'wb').write)
                    time.sleep(1)
                logging.info("DONE")
                print("DONE")
                localpath1 = "D:\\" + folder_name1
                logging.info("Synchronizing ftp " + name1 + " and ftp " + name2)
                print("Synchronizing ftp " + name1 + " and ftp " + name2)
                sync_ftps(ftp,folder_name,localpath,ftp1,folder_name1,localpath1)
        except ftplib.error_perm as error:
            print(error)
    elif type2 == "ftp":
        # We will proceed in the following steps exactly like in the case where type1 was "ftp"
        username = name2.split(":")[0]
        password = name2.split(":")[1].split("@")[0]
        server = name2.split(":")[1].split("@")[1].split("/")[0]
        folder_name = name2.split("/")[1]
        try:
            ftp = FTP(server)
            ftp.login(username, password)
            check_dir(ftp, folder_name, "D:\\TESTFTP")
            ftp.cwd('/.')
            logging.info("Getting all files from ftp into a local path...")
            print("Getting all files from ftp into a local path...")
            for f in my_files:
                file_name = f.replace('/', '\\')
                ftp.retrbinary('RETR ' + f, open("D:" + file_name, 'wb').write)
                time.sleep(1)
            logging.info("DONE")
            print("DONE")
            localpath = "D:\\" + folder_name
            if type1 == "folder":
                logging.info("Synchronizing folder " + name1 + " and ftp " + name2)
                print("Synchronizing folder " + name1 + " and ftp " + name2)
                sync_folder_and_ftp(ftp, folder_name, localpath, name1)
            elif type1 == "zip":
                zip = name1 + "zip"
                folder = get_zip_folder(zip)
                prepare_zip_file(zip, folder)
                logging.info("Synchronizing zip " + folder + " and ftp " + name2)
                print("Synchronizing zip " + folder + " and ftp " + name2)
                sync_ftp_and_zip(ftp, folder_name, localpath, folder)
            elif type1 == "ftp":
                username1 = name1.split(":")[0]
                password1 = name1.split(":")[1].split("@")[0]
                server1 = name1.split(":")[1].split("@")[1].split("/")[0]
                folder_name1 = name1.split("/")[1]
                ftp1 = FTP(server1)
                ftp1.login(username1, password1)
                check_dir(ftp1, folder_name1, "D:\\TESTFTP")
                ftp.cwd('/.')
                logging.info("Getting all files from ftp into a local path...")
                print("Getting all files from ftp into a local path...")
                for f in my_files:
                    file_name = f.replace('/', '\\')
                    ftp.retrbinary('RETR ' + f, open("D:" + file_name, 'wb').write)
                    time.sleep(1)
                logging.info("DONE")
                print("DONE")
                localpath1 = "D:\\" + folder_name1
                logging.info("Synchronizing ftp " + name2 + " and ftp " + name1)
                print("Synchronizing ftp " + name2 + " and ftp " + name1)
                sync_ftps(ftp, folder_name, localpath, ftp1, folder_name1, localpath1)
        except ftplib.error_perm as error:
            logging.info(error)
            print(error)
    else:
        logging.error("LOCATION TYPES UNAVAILABLE")
        print("LOCATION TYPES UNAVAILABLE")

rsync(location1,location2)