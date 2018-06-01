import os, sys, re, json, zipfile, filecmp, getopt, os.path,  filecmp
print "Check 1: File in 'morphology' folder has the same name as the value of the key in 'morph.json' in 'config' folder\n", \
"Check 2: Only 1 file is present in 'morphology' folder \n", \
"Check 3: 'features.json', 'morph.json', 'parameters.json', 'protocols.json' files are present in 'config' folder \n", \
"Check 4: The same key is used in all .json files in 'config' folder \n", \
"Check 5: All files with the same name in all 'mechanisms' folders are exact copies \n", \
"Check 6: All the folders have the same structure \n", \
"Check 7: 'analysis.py', 'evaluator.py', 'template.py', '__init__.py' files are present in 'model' folder \n", \
"Check 8: 'get_stats.py', 'task_stats.py' files are present in 'tools' folder \n", \
"Check 9: In 'opt_neuron.py' file, line 75 contains the same key as the one in the .json files in 'config'\n", \
"Check 10: 'Checkpoints' folder has as many .hoc and .pkl files with the same count and name as the seed folders.\n", \
"Check 11: 'Figures' folder has as many 'evolution, 'objectives' and 'responses' files with the same count and name as the seed folders.\n", \

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
    mfiles = os.listdir(os.path.join(optimizations, folder, folder, "morphology"))
    if name.__len__() == 1:
        print "Check 2: Success!"
    else:
        print "Check 2: Fail!"
        print "    Number of files present in 'morphology' folder:", name.__len__()
        print "    Files in 'morphology' folder:"
        for i in range (0,len(mfiles)):
            print "       ", mfiles[i]
    return name.__len__() == 1

def check_three(config_list):
    check_three = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']
    if check_three == config_list:
        print "Check 3: Success!"
    else:
        print "Check 3: Fail!"
        print "    Files present in 'config' folder:"
        for i in range (0,len(config_list)):
            print "       ", config_list[i]
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
    difffile=0
    print_fail_once=1
    for i in range(len(listkeys)):
        foldersofthekey=d.get(listkeys[i])
        for j in range(1,len(foldersofthekey)):
            if not filecmp.cmp(os.path.join(optimizations, foldersofthekey[0], foldersofthekey[0], "mechanisms", listkeys[i]),\
                               os.path.join(optimizations, foldersofthekey[j], foldersofthekey[j], "mechanisms", listkeys[i])):
                if print_fail_once==1:
                    print "\nCheck 5: Fail!"
                    print_fail_once+=1
                print "    ", "File:", listkeys[i], "is not the same in \n",\
                      "    ", foldersofthekey[0],\
                      "    ", "\n     and\n",\
                      "    ", foldersofthekey[j], "\n"
                difffile=1
    if difffile==1:
        return False
    print "Check 5: Success!"
    return True

def check_six (check_folder):
    for folder in os.listdir(optimizations):
        if (not re.match('README', folder)): #Avoid README file
            if not os.path.isdir(os.path.join(optimizations, folder, folder, check_folder)):
                print "\nCheck 6: Fail!"
                print "    ", check_folder, "folder does not exist in directory:", folder
                return False
            else:
                return True

def check_seven(model_list):
    check_seven = ['analysis.py', 'evaluator.py', 'template.py', '__init__.py']
    if check_seven == model_list:
        print "Check 7: Success!"
    else:
        print "Check 7: Fail!"
        print "    Files present in 'model' folder:"
        for i in range (0,len(model_list)):
            print "       ", model_list[i]
    return check_seven == model_list

def check_eight(tools_list):
    check_eight = ['get_stats.py', 'task_stats.py']
    if check_eight == tools_list:
        print "Check 8: Success!"
    else:
        print "Check 8: Fail!"
        print "    Files present in 'tools' folder:"
        for i in range (0,len(tools_list)):
            print "       ", tools_list[i]
    return check_eight == tools_list

def check_nine():
    for line in open(os.path.join(optimizations, folder, folder, "opt_neuron.py")):
         if line.startswith('evaluator = model.evaluator.create'):
             start = "model.evaluator.create('"
             end = "', "
             return line[line.find(start)+len(start):line.rfind(end)]

def check_ten(seed_list, seed_list_fail):
    hoc_list = []
    hoc_list_fail = []
    pkl_list = []
    pkl_list_fail = []

    for y in os.listdir(os.path.join(optimizations, folder, folder, "checkpoints")):
        if '.hoc' in y:
            start = "cell_"
            end = "_0.hoc"
            hoc_list.append(y[y.find(start)+len(start):y.rfind(end)])
            hoc_list_fail.append(y)

    for z in os.listdir(os.path.join(optimizations, folder, folder, "checkpoints")):
        if '.pkl' in z:
            start = ""
            end = ".pkl"
            pkl_list.append(z[z.find(start)+len(start):z.rfind(end)])
            pkl_list_fail.append(z)

    if seed_list == hoc_list == pkl_list:
        print "Check 10: Success!"
    else:
        print "Check 10: Fail!"
        print "    'r_seed' folders:"
        for x in seed_list_fail:
            print "        ", x
        print "    '.hoc' files:"
        for y in hoc_list_fail:
            print "        ", y
        print "    '.pkl' files:"
        for z in pkl_list_fail:
            print "        ", z
    return

def check_eleven(seed_list, seed_list_fail):
    evolution_list = []
    evolution_list_fail = []
    objectives_list = []
    objectives_list_fail = []
    responses_list = []
    responses_list_fail = []
    
    for x in os.listdir(os.path.join(optimizations, folder, folder, "figures")):
        if 'evolution' in x:
            start = "neuron_evolution_"
            end = ".pdf"
            evolution_list.append(x[x.find(start)+len(start):x.rfind(end)])
            evolution_list_fail.append(x)
    for y in os.listdir(os.path.join(optimizations, folder, folder, "figures")):
        if 'objectives' in y:
            start = "neuron_objectives_"
            end = ".pdf"
            objectives_list.append(y[y.find(start)+len(start):y.rfind(end)])
            objectives_list_fail.append(y)

    for z in os.listdir(os.path.join(optimizations, folder, folder, "figures")):
        if 'responses' in z:
            start = "neuron_responses_"
            end = ".pdf"
            responses_list.append(z[z.find(start)+len(start):z.rfind(end)])
            responses_list_fail.append(z)

    if seed_list == evolution_list == objectives_list == responses_list:
        print "Check 11: Success!"
    else:
        print "Check 11: Fail!"
        print "    'r_seed' folders:"
        for q in seed_list_fail:
            print "        ", q
        print "    'evolution' files:"
        for x in evolution_list_fail:
            print "        ", x
        print "    'objectives' files:"
        for y in objectives_list_fail:
            print "        ", y
        print "    'responses' files:"
        for z in responses_list_fail:
            print "        ", z    
        
    return

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
                with open("morph.json") as json_file:
                    morph_data = json.load(json_file)
                    
#Open file in morphology with name json_data[char]
                name = os.listdir(os.path.join(optimizations, folder, folder, "morphology"))
                print "\n\n", folder
                check_one(name,morph_data)
                check_two(name)
                config_list = os.listdir(os.path.join(optimizations, folder, folder, "config"))
                bool_three = check_three(config_list)
                check_four_keys = [check_four("morph.json"), check_four("features.json"), check_four("parameters.json"),check_four("protocols.json")]
                if bool_three is True:   
                    check_four_boolean = (check_four("morph.json") == check_four("features.json") == check_four("parameters.json") == check_four("protocols.json"))
                    if check_four_boolean is True:
                        print "Check 4: Success!"
                    else:
                        
                        print "Check 4: Fail!"
                        print "    The key '",unique_key(check_four_keys),"' in the file:" 
                        if unique_key(check_four_keys) == check_four("morph.json"):
                            print "    'morph.json' does not match the keys in the other files"
                        elif unique_key(check_four_keys) == check_four("features.json"):
                            print "   'features.json' does not match the keys in the other files"
                        elif unique_key(check_four_keys) == check_four("parameters.json"):
                             print "    'parameters.json' does not match the keys in the other files"
                        elif unique_key(check_four_keys) == check_four("protocols.json"):
                            print "    'protocols.json' does not match the keys in the other files"
                else:
                    print "Check 4: Cannot run because Check 3 failed."
                os.chdir(os.path.join('..','..','..'))
                model_list = os.listdir(os.path.join(optimizations, folder, folder, "model"))
                check_seven(model_list)
                tools_list = os.listdir(os.path.join(optimizations, folder, folder, "tools"))
                check_eight(tools_list)
                if check_four_boolean is True:
                    if check_nine() == check_four_keys[0]:
                        print "Check 9: Success!"
                    else:
                        print "Check 9: Fail!"
                        print "    The key in the .json files in 'config' is:", check_four_keys[0]
                        print "    The key in 'opt_neuron.py' file, line 75 is:", check_nine()
                else:
                    print "Check 9: Cannot run because Check 4 failed."
                seed_list = []
                seed_list_fail = []
                for x in os.listdir(os.path.join(optimizations, folder, folder)):
                    if (x.startswith('r_seed')):
                        start = "r_"
                        end = "_0"
                        seed_list.append(x[x.find(start)+len(start):x.rfind(end)])
                        seed_list_fail.append(x)    
                check_ten(seed_list, seed_list_fail)
                check_eleven(seed_list, seed_list_fail)
                           
                    
    
check_five()
check_six_bool = (check_six("checkpoints") == check_six("config") == check_six("figures") == check_six("mechanisms") == check_six("model") == check_six("morphology") == check_six("tools"))
if check_six_bool is True:
    print "\nCheck 6: Success!"
