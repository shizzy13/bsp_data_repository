import os, sys, re, json, zipfile, filecmp, getopt, os.path

#Check if file in morphology folder has the same name as the value in morph.json file in config
def check_one (name,morph_data):
    same_name = 0
    for n in name:
        if n == morph_data.values()[0]:
            same_name += 1
    return same_name == 1
                
#Check if only 1 file is present in morphology
def check_two (name):
    return name.__len__() == 1

#Check if features.json, morph.json, parameters.json, protocols.json files are present in config
def check_three(config_list):
    check_three = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']
    return check_three == config_list

#check if the same key is used in all files in config
def check_four(jjson):
    with open(jjson) as json_file:
        json_data = json.load(json_file)
    return json_data.keys()[0]

def report(check, n):
    if check:
        print "Check", n, "success!"
    else:
        print "Check", n , "fail!"
                        
#Open folder in Optimization
repository = os.path.dirname(os.path.abspath(__file__))
optimizations = os.path.join(repository, "optimizations")


#Extract files in same directory
for folder in os.listdir(optimizations):
    if (re.match('CA1', folder)): #Avoid README file
        curr_folder = os.path.join(optimizations, folder)
        for files in os.listdir(curr_folder):
            if files.endswith('.zip'):
                os.chdir(curr_folder)
                zip_ref = zipfile.ZipFile(files, 'r')
                zip_ref.extractall('.')
                zip_ref.close() 
                os.chdir(os.path.join('..','..'))

#Read .json file
        for files in os.listdir(curr_folder):
            if (files == folder):
                os.chdir(os.path.join(optimizations, folder, folder, "config"))
                config_list = os.listdir('.')
                with open("morph.json") as json_file:
                    morph_data = json.load(json_file)
                
#Open file in morphology with name json_data[char]
                name = os.listdir(os.path.join(optimizations, folder, folder, "morphology"))
                print "\n\n", folder
                same_name=check_one(name,morph_data)
                report(same_name, 1)
                n_files=check_two(name)
                report(n_files, 2)
                check_three_boolean=check_three(config_list)
                report(check_three_boolean, 3)
                if check_three_boolean:   
                    check_four_boolean = (check_four("morph.json") == check_four("features.json") == check_four("parameters.json") == check_four("protocols.json"))
                    report(check_four_boolean, 4)
