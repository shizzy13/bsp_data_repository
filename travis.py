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

                def check_four(jjson):
                    with open(jjson) as json_file:
                        json_data = json.load(json_file)
                    for char in json_data:
#                        print "##(json_data)##", (char)
                        return char        

#Checks
                print "\n\n", folder
                for n in name:
                    if n == morph_data[char]:
                        print "Check 1 success!"
                    else:
                        print "Check 1 fail!"
                        
                if name.__len__() != 1:
                    print "Check 2 fail!"
                    
                else:
                    print "Check 2 success!"
                    
                check_three = ['features.json', 'morph.json', 'parameters.json', 'protocols.json']
                if config_list == check_three:
                    print "Check 3 success!"
                else:
                    print "Check 3 fail!"
                    
                if check_four("morph.json") == check_four("features.json") == check_four("parameters.json") == check_four("protocols.json"):
                    print "Check 4 success!"
                else:
                    print "Check 4 fail!"

                    
                        
                
                

            
            








    

            




        


