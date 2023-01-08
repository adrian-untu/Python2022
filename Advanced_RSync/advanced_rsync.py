import sys
import os
import shutil
import time

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

def continue_sync(path1,path2):
    list_for_path1 = generate_list(path1)
    list_for_path2 = generate_list(path2)
    time.sleep(1)
    list_for_path1_second = generate_list(path1)
    list_for_path2_second = generate_list(path2)
    print(list_for_path1)
    print(list_for_path1_second)
    time.sleep(1)
    print(list_for_path2)
    print(list_for_path2_second)
    if len(list_for_path1_second) > len(list_for_path2_second) and len(list_for_path1) == len(list_for_path2):
        print("list1>list2")
        delete_folders(path2,path1)
    else:
        print("list2>list1")
        syncDirs(path1,path2)
        syncFiles(path1,path2)
        #delete_folders(path1,path2)

def continue_sync_folder_and_zip(folder,zip_folder):
    zip = zip_folder + ".zip"
    prepare_zip_file(zip, zip_folder) #creates folder
    list_for_path1 = generate_list(folder)
    list_for_path2 = generate_list(zip_folder)
    time.sleep(2) #waits 2 seconds to let the script run and get all the files okay
    list_for_path1_second = generate_list(folder)
    list_for_path2_second = generate_list(zip_folder)
    print(list_for_path1)
    print(list_for_path1_second)
    time.sleep(2)
    print(list_for_path2)
    print(list_for_path2_second)
    if len(list_for_path1_second) > len(list_for_path2_second) and len(list_for_path1) == len(list_for_path2):
        print("list1>list2")
        delete_folders(zip_folder, folder)
    else:
        print("list2>list1")
        syncDirs(folder, zip_folder)
        syncFiles(folder, zip_folder)
        # delete_folders(path1,path2)
    zip_file = zip_folder + ".zip"
    os.remove(zip_file)
    shutil.make_archive(zip_folder, "zip", zip_folder)
    for filename in os.listdir(zip_folder):
        file_path = os.path.join(zip_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.rmdir(zip_folder)

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
        continue_sync(path1,path2)

def sync_folder_and_zip(folder,zip_folder):
    print("Doing initial sync...")
    initial_step(folder,zip_folder)
    zip_file = zip_folder + ".zip"
    os.remove(zip_file)
    shutil.make_archive(zip_folder,"zip",zip_folder)
    for filename in os.listdir(zip_folder):
        file_path = os.path.join(zip_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.rmdir(zip_folder)
    print("First sync done, proceeding with sync of files")
    while 1:
        time.sleep(1)
        continue_sync_folder_and_zip(folder,zip_folder)

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
    else:
        print("LOCATION TYPES UNAVAILABLE")

rsync(location1,location2)