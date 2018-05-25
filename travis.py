import os, sys, re, json, zipfile

#Open folder in Optimization
repository = os.path.dirname(os.path.abspath(__file__))
optimizations = os.path.join(repository, "optimizations")

#print repository
#print optimizations

#Extract files in same directory
for folder in os.listdir(optimizations):
    if (re.match('CA1', folder)): #Avoid README file
        curr_folder = os.path.join(optimizations, folder)
#        print "#curr_folder#", curr_folder
#        print "#os.listdir(os.path.join(optimizations, folder))#", os.listdir(os.path.join(optimizations, folder))
#        print "#os.getcwd()#", os.getcwd()
#        print "outside"
#        print "#folder#", folder
        for files in os.listdir(os.path.join(optimizations, folder)):
            if files.endswith('.zip'):
#                print "insidee"
                os.chdir(os.path.join(optimizations, folder))
                zip_ref = zipfile.ZipFile(files, 'r')
                zip_ref.extractall('.')
                zip_ref.close() 
                os.chdir(os.path.join('..','..'))
#            print "#os.getcwd()#", os.getcwd()
#            print "#os.listdir(os.path.join(optimizations, folder))#", os.listdir(os.path.join(optimizations, folder))
           
#Read .json file
        for files in os.listdir(os.path.join(optimizations, folder)):
            if (files == folder):
#                print "##os.getcwd()##", os.getcwd()
                os.chdir(os.path.join(optimizations, folder, folder, "config"))
                config_list = (os.listdir('.'))
#                print "##(os.listdir('.'))##",(os.listdir('.'))
                with open("morph.json") as json_file:
                    morph_data = json.load(json_file)
                for char in morph_data:
#                    print "##(morph_data[char])##", (morph_data[char])
                
#Open file in morphology with name json_data[char]
                    name = os.listdir(os.path.join(optimizations, folder, folder, "morphology"))
#                    print "name", name
                    
#Check if file in morphology folder has the same name as the value in morph.json file in config
                def check_one (same_name = 0):
                    for n in name:
                        if n == morph_data[char]:
                            same_name += 1
                    return same_name
                
#Check if only 1 file is present in morphology
                def check_two (file_count = 1):
                    if file_count == name.__len__():
                        return file_count

#Check if features.json, morph.json, parameters.json, protocols.json files are present in config
                def check_three(check_three = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']):
                    if check_three == config_list:
                        return check_three

#check if the same key is used in all files in config
                def check_four(jjson):
                    with open(jjson) as json_file:
                        json_data = json.load(json_file)
                    for char in json_data:
                        return char
                  
                def report(check, n):
                    if check:
                        print "Check", n, "success!"
                    else:
                        print "Check", n , "fail!"
             
                print "\n\n", folder
                report(check_one(), 1)
                report(check_two(), 2)
                report(check_three(), 3)
                if check_four("morph.json") == check_four("features.json") == check_four("parameters.json") == check_four("protocols.json"):
                    report(1, 4)
                else:
                    report(0, 4)
                
               

                    
                        
                
                

            
            








    

            




        


