import sys
import os

#get the name of the project
if len(sys.argv)< 2:
 print ""
 print "Error, project name not defined"
 print "usage is xxxx"
 print "Aborting"
 sys.exit(0)

project_name = sys.argv[1]

#check the project_name is there
#check that sys.argv[1]

#bail if the name if taken
if os.path.exists(project_name):
 print ""
 print "There is already a file or directory named " + project_name
 print "Aborting"
 sys.exit(0)

#create directories
print "Creating project directory " + project_name
os.mkdir(project_name)
print "Directoy " + project_name + " created\n"

glade_dir = project_name + "/glade"
print "Creating project directory " + glade_dir
os.mkdir(glade_dir)
print "Directoy " + glade_dir + " created\n"

python_dir = project_name + "/python"
print "Creating project directory " + python_dir
os.mkdir(python_dir)
print "Directoy " + python_dir + " created\n"

media_dir = project_name + "/media"
print "Creating project directory " + media_dir
os.mkdir(media_dir)
print "Directoy " + media_dir + " created\n"

#copy files

#set permissions

#run the program

#print next steps


print "finishing"
sys.exit(0)
