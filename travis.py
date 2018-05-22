import os, sys, re

#Open folder in Optimization
opt_path = r"C:\Users\neli\Desktop\TESTYAML\bsp_data_repository\optimizations"
opt_folder = os.listdir(opt_path)

#Attempt to extract files in same directory
for item in opt_folder:
        extension = ".zip"
        if item.endswith(extension):
            zipfile.ZipFile.extractall(os.path.join(opt_path, item))
     
        config_path = os.path.join(opt_path, item, item, "config\morph.json")
        print config_path
        
#Attempt to open morph.json file and get the string that I need      
        with open(config_path,'r') as f:
            data=[]
            flag=False
            for char in f:
                if ' "' in line:
                    flag=True
                if flag:
                    data.append(char)
                if '"}' in line:
                    flag=False

            print ''.join(data)"""
            




        


