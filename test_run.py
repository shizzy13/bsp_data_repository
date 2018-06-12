import os, sys, re, json, zipfile, filecmp, getopt, os.path, pytest

def same_structure (check_folder):
    """Check if all the folders have the same structure"""
    failure_list=[]
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            if not os.path.isdir(os.path.join(repository, "optimizations", folder, folder, check_folder)):
                failure_list.append(check_folder)
                failure_list.append("folder does not exist in directory:")
                failure_list.append(folder)
        return failure_list
    
def validate_json_files(f, folder):
    """Check if .json files in 'config' folder are valid"""
    failure_list = []
    with open(f) as json_file:
        try:
            json_data = json.load(json_file)
            return failure_list
        except ValueError as error:
            failure_list.append(folder)
            failure_list.append(f)
            failure_list.append("Is an invalid json file: %s" % error)
            return failure_list

def files_present_in_config(config_list, folder):
    """Check if 'features.json', 'morph.json', 'parameters.json', 'protocols.json' files are present in 'config' folder"""
    files_present_in_config = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']
    failure_list = []
    if files_present_in_config != config_list:
        failure_list.append (folder)
        failure_list.append ("Files present in 'config' folder:")
        for i in range (0,len(config_list)):
            failure_list.append (config_list[i])
    return failure_list

def files_present_in_model(model_list, folder):
    """Check if 'analysis.py', 'evaluator.py', 'template.py', '__init__.py' files are present in 'model' folder"""
    files_present_in_model = ['__init__.py', 'analysis.py', 'evaluator.py', 'template.py']
    failure_list = []
    if files_present_in_model != model_list:
        failure_list.append (folder)
        failure_list.append ("Files present in 'model' folder:")
        for i in range (0,len(model_list)):
            failure_list.append (model_list[i])
    return failure_list

def files_present_in_tools(tools_list, folder):
    """Check if 'get_stats.py', 'task_stats.py' files are present in 'tools' folder """
    files_present_in_tools = ['get_stats.py', 'task_stats.py']
    failure_list = []
    if files_present_in_tools != tools_list:
        failure_list.append (folder)
        failure_list.append ("Files present in 'tools' folder:")
        for i in range (0,len(tools_list)):
            failure_list.append (tools_list[i])
    return failure_list

def one_file_present_in_morphology (morphology_list, folder):
    """Check if only 1 file is present in 'morphology' folder \n"""
    failure_list = []
    if morphology_list.__len__() != 1:
        failure_list.append(folder)
        failure_list.append("Number of files present in 'morphology' folder:")
        failure_list.append(morphology_list.__len__())
        failure_list.append("Files in 'morphology' folder:")
        for i in range (0,len(morphology_list)):
            failure_list.append(morphology_list[i])
    return failure_list

def correct_filename_in_morphology (morphology_list, morph_data, folder):
    """Check if file in 'morphology' folder has the same name as the value of the key in 'morph.json' in 'config' folder"""
    failure_list = []
    same_name = 0
    for file_name in morphology_list:
        if file_name == morph_data.values()[0]:
            same_name += 1
    if same_name != 1:
        failure_list.append(folder)
        failure_list.append("Name of file in 'morphology' folder:")
        failure_list.append(file_name)
        failure_list.append("Value of the key in morph.json file:")
        failure_list.append(morph_data.values()[0])
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
        failure_list.append(folder)  
        failure_list.append("'r_seed' folders:")
        for x in seed_list_fail:
            failure_list.append(x)
        failure_list.append("'.hoc' files:")
        for y in hoc_list_fail:
            failure_list.append(y)
        failure_list.append("'.pkl' files:")
        for z in pkl_list_fail:
            failure_list.append(z)
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
        failure_list.append(folder)
        failure_list.append("'r_seed' folders:")
        for q in seed_list_fail:
            failure_list.append(q)
        failure_list.append("'evolution' files:")
        for x in evolution_list_fail:
            failure_list.append(x)
        failure_list.append("'objectives' files:")
        for y in objectives_list_fail:
            failure_list.append(y)
        failure_list.append("'responses' files:")
        for z in responses_list_fail:
            failure_list.append(z)   
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
                    failure_list.append("Failed! Check if all files with the same name in all 'mechanisms' folders are exact copies")
                    print_fail_once+=1
                failure_list.append("File:")
                failure_list.append(listkeys[i])
                failure_list.append("is not the same in")
                failure_list.append(foldersofthekey[0])
                failure_list.append("and")
                failure_list.append(foldersofthekey[j])
    return failure_list
                    
"""Test functions"""

def test_same_structure():
    full_failure_list = []
    if same_structure("checkpoints") != []:
        full_failure_list.append(same_structure("checkpoints"))
    if same_structure("config") != []:
        full_failure_list.append(same_structure("config"))
    if same_structure("figures") != []:
        full_failure_list.append(same_structure("figures"))
    if same_structure("mechanisms") != []:
        full_failure_list.append(same_structure("mechanisms"))
    if same_structure("model") != []:
        full_failure_list.append(same_structure("model"))
    if same_structure("morphology") != []:
        full_failure_list.append(same_structure("morphology"))
    if same_structure("tools") != []:
        full_failure_list.append(same_structure("tools"))
    for failure in full_failure_list:
        print failure, "\n"
    assert full_failure_list == []

#if same_structure (check_folder)
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
                        full_failure_list.append(validate_json_files("features.json", folder))
                    if validate_json_files("morph.json", folder) != []:
                        full_failure_list.append(dvalidate_json_files("morph.json", folder))
                    if validate_json_files("parameters.json", folder) != []:
                        full_failure_list.append(validate_json_files("parameters.json", folder))
                    if validate_json_files("protocols.json", folder) != []:
                        full_failure_list.append(validate_json_files("protocols.json", folder))
    for failure in full_failure_list:
        print failure, "\n"
    assert full_failure_list == []

#if same_structure (check_folder), validate_json_files(f, folder)
def test_files_present_in_config():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    config_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "config"))
                    if files_present_in_config(config_list, folder) != []:
                        full_failure_list.append(files_present_in_config(config_list, folder))
        for failure in full_failure_list:
            print failure, "\n"
    assert full_failure_list == []

#if same_structure (check_folder)
def test_files_present_in_model():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):    
                    model_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "model"))
                    if files_present_in_model(model_list, folder) != []:
                        full_failure_list.append(files_present_in_model(model_list, folder))
        for failure in full_failure_list:
            print failure, "\n"
    assert full_failure_list == []
    
#if same_structure (check_folder)
def test_files_present_in_tools():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):    
                    tools_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "tools"))
                    if files_present_in_tools(tools_list, folder) != []:
                        full_failure_list.append(files_present_in_tools(tools_list, folder))
        for failure in full_failure_list:
            print failure, "\n"
    assert full_failure_list == []

#if same_structure (check_folder)
def test_one_file_present_in_morphology():
    full_failure_list = []
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    morphology_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "morphology"))
                    if one_file_present_in_morphology(morphology_list, folder) != []:
                        full_failure_list.append(one_file_present_in_morphology(morphology_list, folder))
            assert full_failure_list == []

#if same_structure (check_folder), validate_json_files(f, folder), one_file_present_in_morphology (morphology_list, folder)
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
                        full_failure_list.append(correct_filename_in_morphology(morphology_list, morph_data, folder))                   
        for failure in full_failure_list:
            print failure, "\n"
    assert full_failure_list == []

#if same_structure (check_folder), validate_json_files(f, folder), files_present_in_config(config_list, folder)
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
                        full_failure_list.append(folder)
                        full_failure_list.append("The key '")
                        full_failure_list.append(get_the_different_key(same_key_in_jsons_keys))
                        full_failure_list.append("' in the file:")
                        if get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("morph.json"):
                            full_failure_list.append("'morph.json' does not match the keys in the other files")
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("features.json"):
                            full_failure_list.append("'features.json' does not match the keys in the other files")
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("parameters.json"):
                             full_failure_list.append("'parameters.json' does not match the keys in the other files")
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("prococols.json"):
                            full_failure_list.append("'protocols.json' does not match the keys in the other files")

#if same_structure (check_folder), validate_json_files(f, folder), files_present_in_config(config_list, folder), same_key_in_jsons(jjson)
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
                        full_failure_list.append(folder)
                        full_failure_list.append("The key in the .json files in 'config' is:")
                        full_failure_list.append(same_key_in_jsons_keys[0])
                        full_failure_list.append("The key in 'opt_neuron.py' file, line 75 is:")
                        full_failure_list.append(key_in_opt_neuron(folder))


#if same_structure (check_folder)
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
                        full_failure_list.append(files_present_in_checkpoints(seed_list, seed_list_fail, folder))
    for failure in full_failure_list:
         print failure, "\n"
    assert full_failure_list == []


#if same_structure (check_folder)
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
                        full_failure_list.append(files_present_in_figures(seed_list, seed_list_fail, folder))
    for failure in full_failure_list:
        print failure, "\n"
    assert full_failure_list == []

#if same_structure (check_folder)
def test_same_name_files_are_copies():
#    print same_name_files_are_copies(), "\n"
    assert  same_name_files_are_copies() == []


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
