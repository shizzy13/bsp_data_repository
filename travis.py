import os, sys, re, json, zipfile, filecmp, getopt, os.path,  filecmp
print "Check 0: .json files in config are valid \n", \
"Check 1: 'features.json', 'morph.json', 'parameters.json', 'protocols.json' files are present in 'config' folder \n", \
"Check 2: 'analysis.py', 'evaluator.py', 'template.py', '__init__.py' files are present in 'model' folder \n", \
"Check 3: 'get_stats.py', 'task_stats.py' files are present in 'tools' folder \n", \
"Check 4: Only 1 file is present in 'morphology' folder \n", \
"Check 5: File in 'morphology' folder has the same name as the value of the key in 'morph.json' in 'config' folder\n", \
"Check 6: The same key is used in all .json files in 'config' folder \n", \
"Check 7: In 'opt_neuron.py' file, line 75 contains the same key as the one in the .json files in 'config'\n", \
"Check 8: 'Checkpoints' folder has as many .hoc and .pkl files with the same count and name as the seed folders.\n", \
"Check 9: 'Figures' folder has as many 'evolution, 'objectives' and 'responses' files with the same count and name as the seed folders.\n", \
"Check 10: All files with the same name in all 'mechanisms' folders are exact copies \n", \
"Check 11: All the folders have the same structure \n", \


def validate_json_files(f, folder):
    """Check if .json files in 'config' folder are valid"""
    with open(f) as json_file:
        try:
            json_data = json.load(json_file)
            return True
        except ValueError as error:
            print "\n\n", folder
            print "Check 0: Fail!"
            print "    ", f
            print("    Is invalid json: %s" % error)
            return False

def files_present_in_config(config_list, folder):
    """Check if 'features.json', 'morph.json', 'parameters.json', 'protocols.json' files are present in 'config' folder"""
    files_present_in_config = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']
    if files_present_in_config != config_list:
        print "\n\n", folder
        print "Check 1: Fail!"
        print "    Files present in 'config' folder:"
        for i in range (0,len(config_list)):
            print "       ", config_list[i]
    return files_present_in_config == config_list

def files_present_in_model(model_list, folder):
    """Check if 'analysis.py', 'evaluator.py', 'template.py', '__init__.py' files are present in 'model' folder"""
    files_present_in_model = ['__init__.py', 'analysis.py', 'evaluator.py', 'template.py']
    if files_present_in_model != model_list:
        print "\n\n", folder
        print "Check 2: Fail!"
        print "    Files present in 'model' folder:"
        for i in range (0,len(model_list)):
            print "       ", model_list[i]
    return files_present_in_model == model_list

def files_present_in_tools(tools_list, folder):
    """Check if 'get_stats.py', 'task_stats.py' files are present in 'tools' folder """
    files_present_in_tools = ['get_stats.py', 'task_stats.py']
    if files_present_in_tools != tools_list:
        print "\n\n", folder
        print "Check 3: Fail!"
        print "    Files present in 'tools' folder:"
        for i in range (0,len(tools_list)):
            print "       ", tools_list[i]
    return files_present_in_tools == tools_list

def one_file_present_in_morphology (name, folder):
    """Check if only 1 file is present in 'morphology' folder \n"""
    mfiles = os.listdir(os.path.join(optimizations, folder, folder, "morphology"))
    if name.__len__() != 1:
        print "\n\n", folder
        print "Check 4: Fail!"
        print "    Number of files present in 'morphology' folder:", name.__len__()
        print "    Files in 'morphology' folder:"
        for i in range (0,len(mfiles)):
            print "       ", mfiles[i]
    return name.__len__() == 1

def correct_filename_in_morphology (name,morph_data, folder):
    """Check if file in 'morphology' folder has the same name as the value of the key in 'morph.json' in 'config' folder"""
    same_name = 0
    for n in name:
        if n == morph_data.values()[0]:
            same_name += 1
    if same_name != 1:
        print "\n\n", folder
        print "Check 5: Fail!"
        print "    Name of file in 'morphology' folder:", n
        print "    Value of the key in morph.json file:", morph_data.values()[0]
    return same_name == 1

                
def same_key_in_jsons(jjson):
    """Get the key used in a .json file in the 'config' folder"""
    with open(jjson) as json_file:
        json_data = json.load(json_file)
    return json_data.keys()[0]

def key_in_opt_neuron():
    """Check if in 'opt_neuron.py' file, line 75 contains the same key as the one in the .json files in 'config'"""
    for line in open(os.path.join(optimizations, folder, folder, "opt_neuron.py")):
         if line.startswith('evaluator = model.evaluator.create'):
             start = "model.evaluator.create('"
             end = "', "
             return line[line.find(start)+len(start):line.rfind(end)]

def files_present_in_checkpoints(seed_list, seed_list_fail, folder):
    """Check if 'Checkpoints' folder has as many .hoc and .pkl files with the same count and name as the seed folders."""
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

    if not seed_list == hoc_list == pkl_list:
        print "\n\n", folder  
        print "Check 8: Fail!"
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

def files_present_in_figures(seed_list, seed_list_fail, folder):
    """Check if 'Figures' folder has as many 'evolution, 'objectives' and 'responses' files with the same count and name as the seed folders"""
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

    if not seed_list == evolution_list == objectives_list == responses_list:
        print "\n\n", folder
        print "Check 9: Fail!"
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

def same_name_files_are_copies():
    """Check if all files with the same name in all 'mechanisms' folders are exact copies"""
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
                    print "\nCheck 10: Fail!"
                    print_fail_once+=1
                print "    ", "File:", listkeys[i], "is not the same in \n",\
                      "    ", foldersofthekey[0],\
                      "    ", "\n     and\n",\
                      "    ", foldersofthekey[j], "\n"
                difffile=1
    if difffile==1:
        return False
    return True


def same_structure (check_folder):
    """Check if all the folders have the same structure"""
    for folder in os.listdir(optimizations):
        if (not re.match('README', folder)): #Avoid README file
            if not os.path.isdir(os.path.join(optimizations, folder, folder, check_folder)):
                print "\n\n", folder
                print "\nCheck 11: Fail!"
                print "    ", check_folder, "folder does not exist in directory:", folder
                return False
            else:
                return True

def get_the_different_key(list1):
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
                validate_json_files_bool = validate_json_files("features.json", folder) == validate_json_files("morph.json", folder)==validate_json_files("parameters.json", folder)==validate_json_files("protocols.json", folder)
                
                with open("morph.json") as json_file:
                    morph_data = json.load(json_file)
                    
#Open file in morphology with name json_data[char]
                name = os.listdir(os.path.join(optimizations, folder, folder, "morphology"))
                config_list = os.listdir(os.path.join(optimizations, folder, folder, "config"))
                files_present_in_config_boolean = files_present_in_config(config_list, folder)
                model_list = os.listdir(os.path.join(optimizations, folder, folder, "model"))
                files_present_in_model(model_list, folder)
                tools_list = os.listdir(os.path.join(optimizations, folder, folder, "tools"))
                files_present_in_tools(tools_list, folder)
                one_file_present_in_morphology(name, folder)
                if validate_json_files_bool is True:
                    correct_filename_in_morphology(name,morph_data, folder)
                else:
                    print "Check 5: Cannot run because Check 0 failed."
                if validate_json_files_bool is False:
                    print "Check 6: Cannot run because Check 0 failed."
                    print "Check 7: Cannot run because Check 0 failed."
                elif files_present_in_config_boolean is False:
                    print "Check 6: Cannot run because Check 1 failed."
                    print "Check 7: Cannot run because Check 1 failed."
                else:    
                    same_key_in_jsons_keys = [same_key_in_jsons("morph.json"), same_key_in_jsons("features.json"), same_key_in_jsons("parameters.json"),same_key_in_jsons("protocols.json")]
                    same_key_in_jsons_boolean = (same_key_in_jsons("morph.json") == same_key_in_jsons("features.json") == same_key_in_jsons("parameters.json") == same_key_in_jsons("protocols.json"))
                    if same_key_in_jsons_boolean is False:
                        print "\n\n", folder
                        print "Check 6: Fail!"
                        print "    The key '",get_the_different_key(same_key_in_jsons_keys),"' in the file:" 
                        if get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("morph.json"):
                            print "    'morph.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("features.json"):
                            print "   'features.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("parameters.json"):
                             print "    'parameters.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("protocols.json"):
                            print "    'protocols.json' does not match the keys in the other files"

                        os.chdir(os.path.join('..','..','..'))
                        if key_in_opt_neuron() != same_key_in_jsons_keys[0]:
                            print "\n\n", folder
                            print "Check 7: Fail!"
                            print "    The key in the .json files in 'config' is:", same_key_in_jsons_keys[0]
                            print "    The key in 'opt_neuron.py' file, line 75 is:", key_in_opt_neuron()
                    if same_key_in_jsons_boolean is False:
                        print "Check 7: Cannot run because Check 6 failed."
                seed_list = []
                seed_list_fail = []
                for x in os.listdir(os.path.join(optimizations, folder, folder)):
                    if (x.startswith('r_seed')):
                        start = "r_"
                        end = "_0"
                        seed_list.append(x[x.find(start)+len(start):x.rfind(end)])
                        seed_list_fail.append(x)    
                files_present_in_checkpoints(seed_list, seed_list_fail, folder)
                files_present_in_figures(seed_list, seed_list_fail, folder)
                
                   
    
same_name_files_are_copies()
same_structure_bool = (same_structure("checkpoints") == same_structure("config") == same_structure("figures") == same_structure("mechanisms") == same_structure("model") == same_structure("morphology") == same_structure("tools"))



os.chdir(os.path.join(optimizations, "CA1_int_bAC_011127HP1_20180120115056", "CA1_int_bAC_011127HP1_20180120115056", "checkpoints"))

