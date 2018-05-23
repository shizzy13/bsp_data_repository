import os, sys, re, json, zipfile

#Open folder in Optimization
repository = os.path.dirname(os.path.abspath(__file__))
optimizations = os.path.join(repository, "optimizations")

print repository
print optimizations

#Extract files in same directory
for folder in os.listdir(optimizations):
    if (re.match('CA1', folder)): #Avoid README file
        curr_folder = os.path.join(optimizations, folder)
        print "###curr_folder###", curr_folder
        print "###os.listdir(os.path.join(optimizations, folder))###", os.listdir(os.path.join(optimizations, folder))
        print "###os.getcwd()###", os.getcwd()
        print "outside"
        print "###folder###", folder
        for files in os.listdir(os.path.join(optimizations, folder)):
            if files.endswith('.zip'):
                print "insidee"
                os.chdir(os.path.join(optimizations, folder))
                zip_ref = zipfile.ZipFile(files, 'r')
                zip_ref.extractall('.')
                zip_ref.close() 
                os.chdir(os.path.join('..','..'))
            print "###os.getcwd()###", os.getcwd()
            print "###os.listdir(os.path.join(optimizations, folder))###", os.listdir(os.path.join(optimizations, folder))
           
#Read .json file
        for files in os.listdir(os.path.join(optimizations, folder)):
            print "###os.getcwd()###", os.getcwd()
            os.chdir(os.path.join(optimizations, folder, folder, "config"))
            print "###(os.listdir('.'))###",(os.listdir('.'))
#            os.chdir(os.path.join('..','..'))
            with open("morph.json") as json_file:
                json_data = json.load(json_file)
            print "(json_data)###########", (json_data)
            os.chdir(os.path.join('..','..'))
            print "os.getcwd()###########", os.getcwd()






    

            




        


