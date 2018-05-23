import os, sys, re, json

#Open folder in Optimization
repository = os.path.dirname(os.path.abspath(__file__))
optimizations = os.path.join(repository, "optimizations")

print "Print repository: \n", repository, "\n\n"
print "Print optimizations: \n", optimizations, "\n\n"

#Attempt to extract files in same directory
for folder in os.listdir(optimizations):
    if (re.match('CA1', folder)): #Avoid README file
        curr_folder = os.path.join(optimizations, folder)
        print curr_folder
        print os.listdir(os.path.join(optimizations, folder))
        print os.getcwd()
        print "out"
        print folder
        if folder.endswith('.zip'):
            print "in"
            os.chdir(os.path.join(optimizations, folder))
            zip_ref = zipfile.ZipFile(folder, 'r')
            zip_ref.extractall('.')
            zip_ref.close() 
            os.chdir(os.path,join('..','..'))
        print os.getcwd()
        print os.listdir(os.path.join(optimizations, folder))
           
#Attempt to read .json file
for folder in os.listdir(optimizations):
    print os.getcwd()
    os.chdir(os.path.join(optimizations, folder, folder))
    print(os.listdir('.'))
    os.chdir(os.path,join('..','..'))
    with open("morph.json") as json_file:
        json_data = json.load(json_file)
    print(json_data)
    os.chdir(os.path,join('..','..'))
    print os.getcwd()






    

            




        


