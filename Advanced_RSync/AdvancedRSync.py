import sys
import os
import shutil

location1 = sys.argv[1]
location2 = sys.argv[2]

def get_type_of_location(location):
    return location.split(":")[0]

def get_location_name(location):
    return (location.split(get_type_of_location(location))[1])[1:]

def initial_setup(path1,path2):
    list_for_path1 = []
    list_for_path2 = []
    for root, dirs, files in os.walk(path1):
        for name in files:
            list_for_path1.append([os.path.join(root,name), os.path.getmtime(os.path.join(root,name))])
        for dir in dirs:
            list_for_path1.append([os.path.join(root,dir), os.path.getmtime(os.path.join(root, dir))])
    for root, dirs, files in os.walk(path2):
        for name in files:
            list_for_path2.append([os.path.join(root,name), os.path.getmtime(os.path.join(root,name))])
        for dir in dirs:
            list_for_path2.append([os.path.join(root,dir), os.path.getmtime(os.path.join(root, dir))])
    for element2, time2 in list_for_path2:
        for element1, time1 in list_for_path1:
            if (element1.replace(path1 , '')) == (element2.replace(path2 , '')):
                if time1 > time2:
                    shutil.copy(element1,element2)
                else:
                    shutil.copy(element2,element1)


def sync_folders(path1, path2):
    while 1:
        initial_setup(path1, path2) #this function will be able to do the initial sync for the requested folders
        #at the moment, it stops while editing the file, I will see what can I do with that

def switch(location1, location2):
    type1 = get_type_of_location(location1)
    type2 = get_type_of_location(location2)
    name1 = get_location_name(location1)
    name2 = get_location_name(location2)
    if type1 == "folder" and type2 == "folder":
        print("Synchronizing folders " + name1 + " and " + name2)
        sync_folders(name1, name2)
    else:
        print("LOCATION TYPES UNAVAILABLE")

switch(location1,location2)