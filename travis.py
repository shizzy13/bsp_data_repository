import os, sys, re, json

#Open folder in Optimization
repository = os.path.dirname(os.path.abspath(__file__))
optimizations = os.path.join(repository, "optimizations")

print repository, "\n\n"
print optimizations, "\n\n"

#Attempt to extract files in same directory
for folder in os.listdir(optimizations):

        if (re.match('CA1', folder)): #Avoid README file
                curr_folder = os.path.join(optimizations, folder)
#                print folder
                extension = ".zip"
                if folder.endswith(extension):
                        zipfile.ZipFile.extractall(os.path.join(optimizations, folder))
                
     
                morph = os.path.join(optimizations, folder, folder, "config\morph.json")
                print morph
     
#Attempt to read .json file     
        with open(morph) as json_data:      
                d = json.load(json_data)
                print(d)




    

            




        


