import sys
import os
import shutil

location1 = sys.argv[1]
location2 = sys.argv[2]

def get_type_of_location(location):
    return location.split(":")[0]

def get_location_name(location):
    return (location.split(get_type_of_location(location))[1])[1:]

def generate_list1(path1):
    list_for_path1 = []
    for root, dirs, files in os.walk(path1):
        for name in files:
            list_for_path1.append([os.path.join(root, name), os.path.getmtime(os.path.join(root, name))])
        for dir in dirs:
            list_for_path1.append([os.path.join(root, dir), os.path.getmtime(os.path.join(root, dir))])
    return list_for_path1

def generate_list2(path2):
    list_for_path2 = []
    for root, dirs, files in os.walk(path2):
        for name in files:
            list_for_path2.append([os.path.join(root, name), os.path.getmtime(os.path.join(root, name))])
        for dir in dirs:
            list_for_path2.append([os.path.join(root, dir), os.path.getmtime(os.path.join(root, dir))])
    return list_for_path2

def new_files_copy (path1, path2):
    list_for_path1 = generate_list1(path1)
    list_for_path2 = generate_list2(path2)
    for element2, time2 in list_for_path2:
        for element1, time1 in list_for_path1:
            if (element1.replace(path1 , '')) == (element2.replace(path2 , '')):
                if time1 > time2:
                    shutil.copy(element1,element2)
                else:
                    shutil.copy(element2,element1)

def initial_setup(path1,path2):
    list_for_path1 = generate_list1(path1)
    list_for_path2 = generate_list2(path2)
    #the first part will handle the folders that have the same path, checking for the newest version among the two
    new_files_copy(path1, path2)
    #the second part will handle the files that are not in the other directory
    for element2, time2 in list_for_path2:
        ok = 0
        for element1, time1 in list_for_path1:
            if (element1.replace(path1 , '')) == (element2.replace(path2 , '')):
                ok = 1
        if ok == 0:
            location_for_copy = get_location_name(location1) + (element2.replace(path2 , ''))
            location_list = location_for_copy.split("\\")
            if len(location_list) > 2:
                location_for_mkdir = get_location_name(location1)
                index = 2
                while index < len(location_list) - 1:
                    location_for_mkdir += "\\" + location_list[index]
                    index += 1
                    print(location_for_mkdir)
                    os.mkdir(location_for_mkdir)
            #shutil.copy(element2, location_for_copy)


def sync_folders(path1, path2):
    initial_setup(path1, path2) #this function will be able to do the initial sync for the requested folders
    print("Initial setup done, proceeding with the sync")
    while 1:
        new_files_copy(path1, path2) #this will take care of the files to be copied to receive the newest version
def rsync(location1, location2):
    type1 = get_type_of_location(location1)
    type2 = get_type_of_location(location2)
    name1 = get_location_name(location1)
    name2 = get_location_name(location2)
    if type1 == "folder" and type2 == "folder":
        print("Synchronizing folders " + name1 + " and " + name2)
        sync_folders(name1, name2)
    else:
        print("LOCATION TYPES UNAVAILABLE")

rsync(location1,location2)