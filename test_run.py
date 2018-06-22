import os, sys, re, json, zipfile, filecmp, getopt, os.path, pytest, pytest_dependency
def get_template_and_hoc_file(folder):
    """Get name of template in the first .hoc file in 'checkpoints' folder"""
    hoc_files = []
    template_name = []
    return_values = []
    os.chdir(os.path.join(repository, "optimizations", folder, folder, "checkpoints"))
    for f in os.listdir(os.path.join(repository, "optimizations", folder, folder, "checkpoints")):
        if f.endswith(".hoc"):
            hoc_files.append(f)
    for c in open(hoc_files[0], "r"):
        start = "begintemplate"
        end = ""
    template_name.append(c[c.find(start)+len(start):c.rfind(end)])
    return_values.append(hoc_files[0])
    return_values.append(template_name[0])
    return return_values
                    
def write_test_hoc (return_values):
    """Write a test.hoc file in each 'checkpoints' folder"""
    hoc_file = return_values[0]
    template_name = return_values[1]
    os.chdir(os.path.join(repository, "optimizations", folder, folder, "checkpoints"))
    file = open("teest.hoc","w")
    file.write("load_file('"+hoc_file+"')\n") 
    file.write("cvode_active(1)\n\n") 
    file.write("objref testcell\n") 
    file.write("testcell = new "+template_name+"()\n\n")
    file.write("testcell.init()") 
    file.close()
    return

def move_files_around(folder):
    """Copy 'morphology' folder and contents from 'mechanisms' to 'checkpoints'"""
    from distutils.dir_util import copy_tree
    os.chdir(os.path.join(repository, "optimizations", folder, folder))
    if not os.path.exists(os.path.join(repository, "optimizations", folder, folder, "checkpoints", "morphology")):
        os.makedirs(os.path.join(repository, "optimizations", folder, folder, "checkpoints", "morphology"))
    copy_tree("morphology", os.path.join(repository, "optimizations", folder, folder, "checkpoints", "morphology"))
    copy_tree("mechanisms", "checkpoints")
    return


"""def change_stuff_in_hoc_file(folder, return_values):
    hoc_file = return_values[0]
    hocc_file = return_values[0]
    asc_file = os.listdir(os.path.join(repository, "optimizations", folder, folder, "checkpoints", "morphology"))
    os.chdir(os.path.join(repository, "optimizations", folder, folder, "checkpoints"))
    f=open(hoc_file,'r')
    lines=f.readlines()
    for i in range(len(lines)):
        if lines[i].startswith('  } else') and lines[i+1].startswith("    load_morphology($s1"):
            lines[i+1]='    load_morphology("morphology", "'+asc_file[0]+'")'
    f=open(hoc_file,'w')
    f.writelines(lines)
    f.close()
    return"""
    

def same_structure (check_folder):
    """Check if all the folders have the same structure"""
    failure_list=[]
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            if not os.path.isdir(os.path.join(repository, "optimizations", folder, folder, check_folder)):
                failure_list.append("fail")
                print "\n\n", folder
                print "\nFailed! All the folders have the same structure"
                print "    ", check_folder, "folder does not exist in directory:", folder
        return failure_list
    
def validate_json_files(f, folder):
    """Check if .json files in 'config' folder are valid"""
    failure_list = []
    with open(f) as json_file:
        try:
            json_data = json.load(json_file)
            return failure_list
        except ValueError as error:
            failure_list.append("fail")
            print "\n\n", folder
            print "Failed! All .json files in 'config' folder are valid"
            print "    ", f
            print("    Is an invalid json: %s" % error)
            return failure_list

def files_present_in_config(config_list, folder):
    """Check if 'features.json', 'morph.json', 'parameters.json', 'protocols.json' files are present in 'config' folder"""
    files_present_in_config = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']
    failure_list = []
    if files_present_in_config != config_list:
        failure_list.append ("fail")
        print "\n\n", folder
        print "Failed! 'features.json', 'morph.json', 'parameters.json', 'protocols.json' files are present in 'config' folder"
        print "    Files present in 'config' folder:"
        for i in range (0,len(config_list)):
            print "       ", config_list[i]
    return failure_list

def files_present_in_model(model_list, folder):
    """Check if 'analysis.py', 'evaluator.py', 'template.py', '__init__.py' files are present in 'model' folder"""
    files_present_in_model = ['__init__.py', 'analysis.py', 'evaluator.py', 'template.py']
    failure_list = []
    if files_present_in_model != model_list:
        failure_list.append ("fail")
        print "\n\n", folder
        print "Failed! 'analysis.py', 'evaluator.py', 'template.py', '__init__.py' files are present in 'model' folder"
        print "    Files present in 'model' folder:"
        for i in range (0,len(model_list)):
            print "       ", model_list[i]
    return failure_list

def files_present_in_tools(tools_list, folder):
    """Check if 'get_stats.py', 'task_stats.py' files are present in 'tools' folder"""
    files_present_in_tools = ['get_stats.py', 'task_stats.py']
    failure_list = []
    if files_present_in_tools != tools_list:
        failure_list.append ("fail")
        print "\n\n", folder
        print "Failed! 'get_stats.py', 'task_stats.py' files are present in 'tools' folder"
        print "    Files present in 'tools' folder:"
        for i in range (0,len(tools_list)):
            print "       ", tools_list[i]
    return failure_list

def one_file_present_in_morphology (morphology_list, folder):
    """Check if only 1 file is present in 'morphology' folder \n"""
    failure_list = []
    if morphology_list.__len__() != 1:
        failure_list.append ("fail")
        print "\n\n", folder
        print "Failed! Only 1 file is present in 'morphology' folder"
        print "    Number of files present in 'morphology' folder:", morphology_list.__len__()
        print "    Files in 'morphology' folder:"
        for i in range (0,len(morphology_list)):
            print "       ", morphology_list[i]
    return failure_list

def correct_filename_in_morphology (morphology_list, morph_data, folder):
    """Check if file in 'morphology' folder has the same name as the value of the key in 'morph.json' in 'config' folder"""
    failure_list = []
    same_name = 0
    for file_name in morphology_list:
        if file_name == morph_data.values()[0]:
            same_name += 1
    if same_name != 1:
        failure_list.append("fail")
        print "\n\n", folder
        print "Failed! File in 'morphology' folder has the same name as the value of the key in 'morph.json' in 'config' folder"
        print "    Name of file in 'morphology' folder:", n
        print "    Value of the key in morph.json file:", morph_data.values()[0]
    return failure_list

def same_key_in_jsons(jjson):
    """Get the key used in a .json file in the 'config' folder"""
    with open(jjson) as json_file:
        json_data = json.load(json_file)
    return json_data.keys()[0]

def key_in_opt_neuron(folder):
    """Check if in 'opt_neuron.py' file, line 75 contains the same key as the one in the .json files in 'config'"""
    for line in open(os.path.join(repository, "optimizations", folder, folder, "opt_neuron.py")):
         if line.startswith('evaluator = model.evaluator.create'):
             start = "model.evaluator.create('"
             end = "', "
             return line[line.find(start)+len(start):line.rfind(end)]

def files_present_in_checkpoints(seed_list, seed_list_fail, folder):
    """Check if 'Checkpoints' folder has as many .hoc and .pkl files with the same count and name as the seed folders."""
    failure_list = []
    hoc_list = []
    hoc_list_fail = []
    pkl_list = []
    pkl_list_fail = []

    for y in os.listdir(os.path.join(repository, "optimizations", folder, folder, "checkpoints")):
        if '.hoc' in y:
            start = "cell_"
            end = "_0.hoc"
            hoc_list.append(y[y.find(start)+len(start):y.rfind(end)])
            hoc_list_fail.append(y)

    for z in os.listdir(os.path.join(repository, "optimizations", folder, folder, "checkpoints")):
        if '.pkl' in z:
            start = ""
            end = ".pkl"
            pkl_list.append(z[z.find(start)+len(start):z.rfind(end)])
            pkl_list_fail.append(z)

    if not seed_list == hoc_list == pkl_list:
        failure_list.append("fail")  
        print "\n\n", folder  
        print "Failed! 'Checkpoints' folder has as many .hoc and .pkl files with the same count and name as the seed folders"
        print "    'r_seed' folders:"
        for x in seed_list_fail:
            print "        ", x
        print "    '.hoc' files:"
        for y in hoc_list_fail:
            print "        ", y
        print "    '.pkl' files:"
        for z in pkl_list_fail:
            print "        ", z
    return failure_list

def files_present_in_figures(seed_list, seed_list_fail, folder):
    """Check if 'Figures' folder has as many 'evolution, 'objectives' and 'responses' files with the same count and name as the seed folders"""
    failure_list = []
    evolution_list = []
    evolution_list_fail = []
    objectives_list = []
    objectives_list_fail = []
    responses_list = []
    responses_list_fail = []
    
    for x in os.listdir(os.path.join(repository, "optimizations", folder, folder, "figures")):
        if 'evolution' in x:
            start = "neuron_evolution_"
            end = ".pdf"
            evolution_list.append(x[x.find(start)+len(start):x.rfind(end)])
            evolution_list_fail.append(x)
    for y in os.listdir(os.path.join(repository, "optimizations", folder, folder, "figures")):
        if 'objectives' in y:
            start = "neuron_objectives_"
            end = ".pdf"
            objectives_list.append(y[y.find(start)+len(start):y.rfind(end)])
            objectives_list_fail.append(y)

    for z in os.listdir(os.path.join(repository, "optimizations", folder, folder, "figures")):
        if 'responses' in z:
            start = "neuron_responses_"
            end = ".pdf"
            responses_list.append(z[z.find(start)+len(start):z.rfind(end)])
            responses_list_fail.append(z)

    if not seed_list == evolution_list == objectives_list == responses_list:
        failure_list.append("fail")
        print "\n\n", folder
        print "Failed! 'Figures' folder has as many 'evolution, 'objectives' and 'responses' files (with proper names) as the seed folders"
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
    return failure_list

def same_name_files_are_copies():
    """Check if all files with the same name in all 'mechanisms' folders are exact copies"""
    failure_list=[]
    listkeys=[]
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for f in os.listdir(os.path.join(repository, "optimizations", folder, folder, "mechanisms")):
                if f not in listkeys:
                    listkeys.append(f)
    d=dict((el,[]) for el in listkeys)
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for f in os.listdir(os.path.join(repository, "optimizations", folder, folder, "mechanisms")):
                d[f].append(folder)
    print_fail_once=1
    for i in range(len(listkeys)):
        foldersofthekey=d.get(listkeys[i])
        for j in range(1,len(foldersofthekey)):
            if not filecmp.cmp(os.path.join(repository, "optimizations", foldersofthekey[0], foldersofthekey[0], "mechanisms", listkeys[i]),\
                               os.path.join(repository, "optimizations", foldersofthekey[j], foldersofthekey[j], "mechanisms", listkeys[i])):
                if print_fail_once==1:
                    failure_list.append("fail")
                    print_fail_once+=1
                    print "\nFailed! All files with the same name in all 'mechanisms' folders are exact copies"
                    print_fail_once+=1
                print "    ", "File:", listkeys[i], "is not the same in \n",\
                      "    ", foldersofthekey[0],\
                      "    ", "\n     and\n",\
                      "    ", foldersofthekey[j], "\n"
    return failure_list
                    
"""Test functions"""

@pytest.mark.dependency()
def test_same_structure():
    full_failure_list = []
    if same_structure("checkpoints") != []:
        full_failure_list.append("fail")
    if same_structure("config") != []:
        full_failure_list.append("fail")
    if same_structure("figures") != []:
        full_failure_list.append("fail")
    if same_structure("mechanisms") != []:
        full_failure_list.append("fail")
    if same_structure("model") != []:
        full_failure_list.append("fail")
    if same_structure("morphology") != []:
        full_failure_list.append("fail")
    if same_structure("tools") != []:
        full_failure_list.append("fail")
    assert full_failure_list == []

@pytest.mark.dependency(depends=["test_same_structure"])
def test_validate_json_files():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    os.chdir(os.path.join(repository, "optimizations", folder, folder, "config"))
                    validate_json_files_bool = validate_json_files("features.json", folder) == validate_json_files("morph.json", folder)==\
                                               validate_json_files("parameters.json", folder)==validate_json_files("protocols.json", folder)
                    if validate_json_files("features.json", folder) != []:
                        full_failure_list.append("fail")
                    if validate_json_files("morph.json", folder) != []:
                        full_failure_list.append("fail")
                    if validate_json_files("parameters.json", folder) != []:
                        full_failure_list.append("fail")
                    if validate_json_files("protocols.json", folder) != []:
                        full_failure_list.append("fail")
    assert full_failure_list == []


@pytest.mark.dependency(depends=["test_same_structure, test_validate_json_files"])
def test_files_present_in_config():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    config_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "config"))
                    if files_present_in_config(config_list, folder) != []:
                        full_failure_list.append("fail")
    assert full_failure_list == []

@pytest.mark.dependency(depends=["test_same_structure"])
def test_files_present_in_model():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):    
                    model_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "model"))
                    if files_present_in_model(model_list, folder) != []:
                        full_failure_list.append("fail")
    assert full_failure_list == []
    
@pytest.mark.dependency(depends=["test_same_structure"])
def test_files_present_in_tools():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):    
                    tools_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "tools"))
                    if files_present_in_tools(tools_list, folder) != []:
                        full_failure_list.append("fail")
    assert full_failure_list == []

@pytest.mark.dependency(depends=["test_same_structure"])
def test_one_file_present_in_morphology():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    morphology_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "morphology"))
                    if one_file_present_in_morphology(morphology_list, folder) != []:
                        full_failure_list.append("fail")
            assert full_failure_list == []

@pytest.mark.dependency(depends=["test_same_structure, test_validate_json_files, test_one_file_present_in_morphology"])
def test_correct_filename_in_morphology():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    os.chdir(os.path.join(repository, "optimizations", folder, folder, "config"))
                    with open("morph.json") as json_file:
                        morph_data = json.load(json_file)
                        morphology_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "morphology"))
                    if correct_filename_in_morphology(morphology_list, morph_data, folder) != []:
                        full_failure_list.append("fail")                   
    assert full_failure_list == []

@pytest.mark.dependency(depends=["test_same_structure, test_validate_json_files, test_files_present_in_config"])
def test_same_key_in_jsons():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    os.chdir(os.path.join(repository, "optimizations", folder, folder, "config"))
                    same_key_in_jsons_keys = [same_key_in_jsons("morph.json"), same_key_in_jsons("features.json"), \
                                                  same_key_in_jsons("parameters.json"),same_key_in_jsons("protocols.json")]
                    same_key_in_jsons_boolean = (same_key_in_jsons("morph.json") == \
                                                 same_key_in_jsons("features.json") == \
                                                 same_key_in_jsons("parameters.json") == \
                                                 same_key_in_jsons("protocols.json"))
                    if same_key_in_jsons_boolean is False:
                        full_failure_list.append("fail")
                        print "\n\n", folder
                        print "Failed! The same key is used in all .json files in 'config' folder"
                        print "    The key '",get_the_different_key(same_key_in_jsons_keys),"' in the file:" 
                        if get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("morph.json"):
                            print "    'morph.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("features.json"):
                            print "   'features.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("parameters.json"):
                             print "    'parameters.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("protocols.json"):
                            print "    'protocols.json' does not match the keys in the other files"
    assert full_failure_list == [] 

@pytest.mark.dependency(depends=["test_same_structure, test_validate_json_files, test_files_present_in_config, test_same_key_in_jsons"])
def test_key_in_opt_neuron():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    os.chdir(os.path.join(repository, "optimizations", folder, folder, "config"))
                    same_key_in_jsons_keys = [same_key_in_jsons("morph.json"), same_key_in_jsons("features.json"), \
                                                  same_key_in_jsons("parameters.json"),same_key_in_jsons("protocols.json")]
                    os.chdir(os.path.join('..','..','..'))
                    if key_in_opt_neuron(folder) != same_key_in_jsons_keys[0]:
                        full_failure_list.append("fail")
                        print "\n\n", folder
                        print "Failed! In 'opt_neuron.py' file, line 75 contains the same key as the one in the .json files in 'config'!"
                        print "    The key in the .json files in 'config' is:", same_key_in_jsons_keys[0]
                        print "    The key in 'opt_neuron.py' file, line 75 is:", key_in_opt_neuron()
    assert full_failure_list == []

@pytest.mark.dependency(depends=["test_same_structure"])
def test_files_present_in_checkpoints():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    seed_list = []
                    seed_list_fail = []
                    for x in os.listdir(os.path.join(repository, "optimizations", folder, folder)):
                        if (x.startswith('r_seed')):
                            start = "r_"
                            end = "_0"
                            seed_list.append(x[x.find(start)+len(start):x.rfind(end)])
                            seed_list_fail.append(x)    
                    if files_present_in_checkpoints(seed_list, seed_list_fail, folder) != []:
                        full_failure_list.append("fail")
    assert full_failure_list == []

@pytest.mark.dependency(depends=["test_same_structure"])
def test_files_present_in_figures():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    seed_list = []
                    seed_list_fail = []
                    for x in os.listdir(os.path.join(repository, "optimizations", folder, folder)):
                        if (x.startswith('r_seed')):
                            start = "r_"
                            end = "_0"
                            seed_list.append(x[x.find(start)+len(start):x.rfind(end)])
                            seed_list_fail.append(x)    
                    if files_present_in_figures(seed_list, seed_list_fail, folder) != []:
                        full_failure_list.append("fail")
    assert full_failure_list == []

@pytest.mark.dependency(depends=["test_same_structure"])
def test_same_name_files_are_copies():
    assert  same_name_files_are_copies() == []

@pytest.mark.dependency()
def test_neuron():
    n=1
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    write_test_hoc (return_values)
                    move_files_around(folder)
                    change_stuff_in_hoc_file(folder, return_values)
                    os.chdir(os.path.join(repository, "optimizations", folder, folder, "checkpoints"))
                    nrnivmodl
    assert n==1
    
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

repository = os.path.dirname(os.path.abspath(__file__))
for folder in os.listdir(os.path.join(repository, "optimizations")):
    if (not re.match('README', folder)): #Avoid README file
        for files in os.listdir(os.path.join(repository, "optimizations", folder)):
            if files.endswith('.zip'):
                os.chdir(os.path.join(repository, "optimizations", folder))
                zip_ref = zipfile.ZipFile(files, 'r')
                zip_ref.extractall('.')
                zip_ref.close() 
                os.chdir(os.path.join('..','..'))
