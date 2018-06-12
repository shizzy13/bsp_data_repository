import os, sys, re, json, zipfile, filecmp, getopt, os.path, pytest

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

"""def same_key_in_jsons(jjson):
    Get the key used in a .json file in the 'config' folder
    with open(jjson) as json_file:
        json_data = json.load(json_file)
    return json_data.keys()[0]"""


"""Test functions"""

def test_validate_json_files():
    repository = os.path.dirname(os.path.abspath(__file__))
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
                        full_failure_list.appen(dvalidate_json_files("morph.json", folder))
                    if validate_json_files("parameters.json", folder) != []:
                        full_failure_list.append(validate_json_files("parameters.json", folder))
                    if validate_json_files("protocols.json", folder) != []:
                        full_failure_list.append(validate_json_files("protocols.json", folder))
    for failure in full_failure_list:
        print failure, "\n"
    assert full_failure_list == []

def test_files_present_in_config():
    repository = os.path.dirname(os.path.abspath(__file__))
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

def test_files_present_in_model():
    repository = os.path.dirname(os.path.abspath(__file__))
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
    
def test_files_present_in_tools():
    repository = os.path.dirname(os.path.abspath(__file__))
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

def test_one_file_present_in_morphology():
    full_failure_list = []
    repository = os.path.dirname(os.path.abspath(__file__))
    for folder in os.listdir(os.path.join(repository, "optimizations")):
        if (not re.match('README', folder)): #Avoid README file
            for files in os.listdir(os.path.join(repository, "optimizations", folder)):
                if (files == folder):
                    morphology_list = os.listdir(os.path.join(repository, "optimizations", folder, folder, "morphology"))
                    if one_file_present_in_morphology(morphology_list, folder) != []:
                        full_failure_list.append(one_file_present_in_morphology(morphology_list, folder))
            assert full_failure_list == []

#if check 1 passes
def test_correct_filename_in_morphology():
    repository = os.path.dirname(os.path.abspath(__file__))
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


"""def test_same_key_in_jsons():
    repository = os.path.dirname(os.path.abspath(__file__))
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
                        full_failure_list.append("The key '", get_the_different_key(same_key_in_jsons_keys),"' in the file:") 
                        if get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("morph.json"):
                            print "    'morph.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("features.json"):
                            print "   'features.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("parameters.json"):
                             print "    'parameters.json' does not match the keys in the other files"
                        elif get_the_different_key(same_key_in_jsons_keys) == same_key_in_jsons("protocols.json"):
                            print "    'protocols.json' does not match the keys in the other files"""


"""repository = os.path.dirname(os.path.abspath(__file__))
for folder in os.listdir(os.path.join(repository, "optimizations")):
    if (not re.match('README', folder)): #Avoid README file
        for files in os.listdir(os.path.join(repository, "optimizations", folder)):
            if files.endswith('.zip'):
                os.chdir(os.path.join(repository, "optimizations", folder))
                zip_ref = zipfile.ZipFile(files, 'r')
                zip_ref.extractall('.')
                zip_ref.close() 
                os.chdir(os.path.join('..','..'))"""
