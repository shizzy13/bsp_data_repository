import os, sys, re, json, zipfile, filecmp, getopt, os.path,  filecmp
print "Check 6: File in 'morphology' folder has the same name as the value of the key in 'morph.json' in 'config' folder\n", \
"Check 5: Only 1 file is present in 'morphology' folder \n", \
"Check 2: 'features.json', 'morph.json', 'parameters.json', 'protocols.json' files are present in 'config' folder \n", \
"Check 7: The same key is used in all .json files in 'config' folder \n", \
"Check 9: All files with the same name in all 'mechanisms' folders are exact copies \n", \
"Check 1: All the folders have the same structure \n", \
"Check 3: 'analysis.py', 'evaluator.py', 'template.py', '__init__.py' files are present in 'model' folder \n", \
"Check 4: 'get_stats.py', 'task_stats.py' files are present in 'tools' folder \n",\
"Check 8: In 'opt_neuron.py' file, line 75 contains the same key as the one in the .json files in 'config'",\

def check_6 (name,morph_data):
    same_name = 0
    for n in name:
        if n == morph_data.values()[0]:
            same_name += 1
    if same_name == 1:
        print "Check 6: Success!"
    else:
        print "Check 6: Fail!"
        print "    Name of file in 'morphology' folder:", n
        print "    Value of the key in morph.json file:", morph_data.values()[0]
    return same_name == 1
                
def check_5 (name):
    mfiles = os.listdir(os.path.join(optimizations, folder, folder, "morphology"))
    if name.__len__() == 1:
        print "Check 5: Success!"
    else:
        print "Check 5: Fail!"
        print "    Number of files present in 'morphology' folder:", name.__len__()
        print "    Files in 'morphology' folder:"
        for i in range (0,len(mfiles)):
            print "       ", mfiles[i]
    return name.__len__() == 1

def check_2(config_list):
    check_2 = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']
    if check_2 == config_list:
        print "Check 2: Success!"
    else:
        print "Check 2: Fail!"
        print "    Files present in 'config' folder:"
        for i in range (0,len(config_list)):
            print "       ", config_list[i]
    return check_2 == config_list

def check_7(jjson):
    with open(jjson) as json_file:
        json_data = json.load(json_file)
    return json_data.keys()[0]

def check_9():
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
    difffile=0
    print_fail_once=1
    for i in range(len(listkeys)):
        foldersofthekey=d.get(listkeys[i])
        for j in range(1,len(foldersofthekey)):
            if not filecmp.cmp(os.path.join(optimizations, foldersofthekey[0], foldersofthekey[0], "mechanisms", listkeys[i]),\
                               os.path.join(optimizations, foldersofthekey[j], foldersofthekey[j], "mechanisms", listkeys[i])):
                if print_fail_once==1:
                    print "\nCheck 9: Fail!"
                    print_fail_once+=1
                print "    ", "File:", listkeys[i], "is not the same in \n",\
                      "    ", foldersofthekey[0],\
                      "    ", "\n     and\n",\
                      "    ", foldersofthekey[j], "\n"
                difffile=1
    if difffile==1:
        return False
    print "Check 9: Success!"
    return True

def check_1 (check_folder):
    for folder in os.listdir(optimizations):
        if (not re.match('README', folder)): #Avoid README file
            if not os.path.isdir(os.path.join(optimizations, folder, folder, check_folder)):
                print "\nCheck 1: Fail!"
                print "    ", check_folder, "folder does not exist in directory:", folder
                return False
            else:
                return True

def check_3(model_list):
    check_3 = ['analysis.py', 'evaluator.py', 'template.py', '__init__.py']
    if check_3 == model_list:
        print "Check 3: Success!"
    else:
        print "Check 3: Fail!"
        print "    Files present in 'model' folder:"
        for i in range (0,len(model_list)):
            print "       ", model_list[i]
    return check_3 == model_list

def check_4(tools_list):
    check_4 = ['get_stats.py', 'task_stats.py']
    if check_4 == tools_list:
        print "Check 4: Success!"
    else:
        print "Check 4: Fail!"
        print "    Files present in 'tools' folder:"
        for i in range (0,len(tools_list)):
            print "       ", tools_list[i]
    return check_4 == tools_list

def check_8():
    for line in open(os.path.join(optimizations, folder, folder, "opt_neuron.py")):
         if line.startswith('evaluator = model.evaluator.create'):
             start = "model.evaluator.create('"
             end = "', "
             return line[line.find(start)+len(start):line.rfind(end)]
    

def unique_key(list1):
    unique_list = []
    repeat_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
        else:
            repeat_list.append(x)
    for x in unique_list:
        if x not in repeat_list:
            return x
     

#Extract files in same directory                   
repository = os.path.dirname(os.path.abspath(__file__))
optimizations = os.path.join(repository, "optimizations")
for folder in os.listdir(optimizations):
    if (not re.match('README', folder)): #Avoid README file
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
                with open("morph.json") as json_file:
                    morph_data = json.load(json_file)
            os.chdir(os.path.join('..','..','..'))
for folder in os.listdir(optimizations):
    if (not re.match('README', folder)): #Avoid README file
        for files in os.listdir(curr_folder):
            if (files == folder):
#Open file in morphology with name json_data[char]
                name = os.listdir(os.path.join(optimizations, folder, folder, "morphology"))
                print "\N\n", folder
                config_list = os.listdir(os.path.join(optimizations, folder, folder, "config"))
                bool_two = check_2(config_list)
                model_list = os.listdir(os.path.join(optimizations, folder, folder, "model"))
                check_3(model_list)
                tools_list = os.listdir(os.path.join(optimizations, folder, folder, "tools"))
                check_4(tools_list)
                check_5(name)
                check_6(name,morph_data)
                check_7_keys = [check_7("morph.json"), check_7("features.json"), check_7("parameters.json"),check_7("protocols.json")]
                if bool_two is True:   
                    check_7_boolean = (check_7("morph.json") == check_7("features.json") == check_7("parameters.json") == check_7("protocols.json"))
                    if check_7_boolean is True:
                        print "Check 7: Success!"
                    else:
                        print "Check 7: Fail!"
                        print "    The key '",unique_key(check_7_keys),"' in the file:" 
                        if unique_key(check_7_keys) == check_7("morph.json"):
                            print "    'morph.json' does not match the keys in the other files"
                        elif unique_key(check_7_keys) == check_7("features.json"):
                            print "   'features.json' does not match the keys in the other files"
                        elif unique_key(check_7_keys) == check_7("parameters.json"):
                             print "    'parameters.json' does not match the keys in the other files"
                        elif unique_key(check_7_keys) == check_7("protocols.json"):
                            print "    'protocols.json' does not match the keys in the other files"
                else:
                    print "Check 7: Cannot run because Check 2 failed."
                if check_7_boolean is True:
                    if check_8() == check_7_keys[0]:
                        print "Check 8: Success!"
                    else:
                        print "Check 8: Fail!"
                        print "    The key in the .json files in 'config' is:", check_7_keys[0]
                        print "    The key in 'opt_neuron.py' file, line 75 is:", check_8()
                else:
                    print "Check 8: Cannot run because Check 4 failed."
check_9()


