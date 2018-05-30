import os, sys, re, json, zipfile, filecmp, getopt, os.path,  filecmp
print "Check 1: File in 'morphology' folder has the same name as the value of the key in 'morph.json' in 'config' folder\n", \
"Check 2: Only 1 file is present in 'morphology' folder \n", \
"Check 3: features.json, morph.json, parameters.json, protocols.json files are present in config \n", \
"Check 4: The same key is used in all .json files in 'config' folder \n", \
"Check 5: All files with the same name in all 'mechanisms' folders are exact copies \n", \
"Check 6: All the folders have the same structure \n", \

def check_one (name,morph_data):
    same_name = 0
    for n in name:
        if n == morph_data.values()[0]:
            same_name += 1
    if same_name == 1:
        print "Check 1: Success!"
    else:
        print "Check 1: Fail!"
        print "    Name of file in 'morphology' folder:", n
        print "    Value of the key in morph.json file:", morph_data.values()[0]
    return same_name == 1
                
def check_two (name):
    if name.__len__() == 1:
        print "Check 2: Success!"
    else:
        print "Check 2: Fail!"
        print "    Number of files present in 'morphology' folder:", name.__len__()
    return name.__len__() == 1

def check_three(config_list):
    check_three = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']
    if check_three == config_list:
        print "Check 3: Success!"
    else:
        print "Check 3: Fail!"
        print "    Files present in 'config' folder:", config_list
    return check_three == config_list

def check_four(jjson):
    with open(jjson) as json_file:
        json_data = json.load(json_file)
    return json_data.keys()[0]

def check_five():
    listkeys=[]
    for folder in os.listdir(optimizations):
        if (not re.match('README', folder)): #Avoid README file
            for f in os.listdir(os.path.join(optimizations, folder, folder, "mechanisms")):
                if f not in listkeys:
                    listkeys.append(f)
    d=dict((el,[]) for el in listkeys)
    for folder in os.listdir(optimizations):
        if (not re.match('README', folder)): #Avoid README file
            for f in os.listdir(os.path.join(optimizations, folder, folder, "mechanisms")):
                d[f].append(folder)
    for i in range(len(listkeys)):
        foldersofthekey=d.get(listkeys[i])
        for j in range(1,len(foldersofthekey)):
            if not filecmp.cmp(os.path.join(optimizations, foldersofthekey[0], foldersofthekey[0], "mechanisms"),\
                               os.path.join(optimizations, foldersofthekey[j], foldersofthekey[j], "mechanisms"),\
                               listkeys[i]):
                print "\nCheck 5: Fail!"
                print "    ", "File:", listkeys[i], "is not the same in \n",\
                      "    ", os.path.join(optimizations, foldersofthekey[0], foldersofthekey[0], "mechanisms\n"),\
                      "    ", "and\n",\
                      "    ", os.path.join(optimizations, foldersofthekey[j], foldersofthekey[j], "mechanisms")
                return True
            else:
                print "Check 5: Success!"
        return  False

def check_six (check_folder):
    for folder in os.listdir(optimizations):
        if (not re.match('README', folder)): #Avoid README file
            if not os.path.isdir(os.path.join(optimizations, folder, folder, check_folder)):
                print "\nCheck 6: Fail!"
                print "    ", check_folder, "folder does not exist in", os.path.join(optimizations, folder, folder)
                return False
            else:
                return True


#Extract files in same directory                   
repository = os.path.dirname(os.path.abspath(__file__))
optimizations = os.path.join(repository, "optimizations")
for folder in os.listdir(optimizations):
    if (not re.match('README', folder)): #Avoid README file
        curr_folder = os.path.join(optimizations, folder)
        """for files in os.listdir(curr_folder):
            if files.endswith('.zip'):
                os.chdir(curr_folder)
                zip_ref = zipfile.ZipFile(files, 'r')
                zip_ref.extractall('.')
                zip_ref.close() 
                os.chdir(os.path.join('..','..'))"""

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
                check_one(name,morph_data)
                check_two(name)
                bool_three = check_three(config_list)
                if bool_three is True:   
                    check_four_boolean = (check_four("morph.json") == check_four("features.json") == check_four("parameters.json") == check_four("protocols.json"))
                    if check_four_boolean is True:
                        print "Check 4: Success!"
                    else:
                        print "Check 4: Fail!"
                        print "    ", check_four("morph.json"), " is the key in in 'morph.json'"
                        print "    ", check_four("features.json"), " is the key in in 'features.json'"
                        print "    ", check_four("parameters.json"), " is the key in in 'parameters.json'"
                        print "    ", check_four("protocols.json"), " is the key in in 'protocols.json'"      
                else:
                    print "Check 4: Cannot run because Check 3 failed."
                os.chdir(os.path.join('..','..','..'))
    
check_five()
check_six_bool = (check_six("checkpoints") == check_six("config") == check_six("figures") == check_six("mechanisms") == check_six("model") == check_six("morphology") == check_six("tools"))
if check_six_bool is True:
    print "\nCheck 6: Success!"
