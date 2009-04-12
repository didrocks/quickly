import sys
import os

#get the name of the project
if len(sys.argv)< 2:
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

print "Creating project directory " + project_name
os.mkdir(project_name)
print "Directoy " + project_name + " created"


print "finishing"
sys.exit(0)
