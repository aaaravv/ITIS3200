#imports

import os
import json
import hashlib
from  pathlib import Path

#Body of code
def main():
    print("1 - Generate new hash table")
    print("2 - Verify hashes")

    job = int(input("Enter: "))

    if job == 1:
        path = input("Enter directory path: ")
        generate_table(path)
       

    elif job == 2:
        path = input("Enter directory path: ")
        validate_hash(path)


#Takes in a file's filepath as input, reads its contents in binary form, and returns its hash(sha256) in hex form, i learned that its good format for comparing hashes
def hash_file(filepath):
    with open(filepath, "rb") as file:
        file_content = file.read()
    return hashlib.sha256(file_content).hexdigest()

#iterates through every object in a directory, if its a file it gets appended to the file list, and its hash gets appended to the hash list
#then the two lists get turned into a dictionary using the zip method, and the dictionary is returned
def traverse_directory(filepath):
    p  = Path(filepath)
    file_list = []
    hash_list = []
    
    for ele in p.iterdir():
        if ele.is_file():
            file_list.append(str(ele))
            hash_list.append(hash_file(ele))
    table = dict(zip(file_list, hash_list))
    return table

    
#takes the dictionary returned when traverse_directory is called, reads through it, turns it into a json format string
#string is then turned into a file, i read that i can directly write to a json file, skipping the json string using dump instead of dumps
#but i didnt want to mess with the code too much, as its late and this seems stable     
def generate_table(filepath):
    hash_table = json.dumps(traverse_directory(filepath))

    with open("hash_table.json", "w") as file:
        file.write(hash_table)
    print("Hash table generated")

#opens the json file, extracts the dictionary from it
def validate_hash(filepath):
    with open("hash_table.json", "r") as file:
        hash_dict = json.load(file)
    
    curr_directory = traverse_directory(filepath)

    #iterates throguh every path in the directory
    for path in hash_dict:
        #if path in directory check if its unchanged
        if path in curr_directory:
            if(hash_dict[path] == curr_directory[path]):
                print(path + " - valid")
            else:
                print(path + " - invalid")
        #if it wasnt in the new dict the file has been deleted
        else:
            print(path + " has been deleted")
    
    #iterates through every file in the new dict, if it wasnt in the old dict its a new file
    for path in curr_directory:
        if path not in hash_dict:
            print(path + " is a new file")

if __name__ == "__main__":
    main()
