import sys
import os
import shutil
import subprocess

def file_from_template(template_dir, template_file, target_dir, project_name, rename = False):
 if rename:
  frags = template_file.split(".")
  target_file = project_name
  if len(frags) > 1:
   target_file += "." + frags[1]
 else:
  target_file = template_file

 print "Creating " + target_dir + "/" + target_file
 fin = open(template_dir + template_file,'r')
 file_contents1 = fin.read().replace("project_name",project_name)
 fout = open(target_dir + target_file, 'w')
 fout.write(file_contents1)
 fout.flush()
 fout.close()
 fout.close()
 print target_dir + "/" + target_file + " created\n"
 
#get the name of the project
if len(sys.argv)< 2:
 print ""
 print "Error, project name not defined"
 print "usage is xxxx"
 print "Aborting"
 sys.exit(0)

pathname = os.path.dirname(sys.argv[0])
abs_path =  os.path.abspath(pathname)

project_name = sys.argv[1]

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
template_glade_dir = abs_path + "/glade/"
target_glade_dir = project_name + "/glade/"
file_from_template(template_glade_dir, "project_name.glade", target_glade_dir, project_name, True)
file_from_template(template_glade_dir, "about.glade", target_glade_dir, project_name)

template_python_dir = abs_path + "/python/"
target_python_dir = project_name + "/python/"
file_from_template(template_python_dir, "project_name.py", target_python_dir, project_name, True)
file_from_template(template_python_dir, "about.py", target_python_dir, project_name)

template_media_dir = abs_path + "/media/"
target_media_dir = project_name + "/media/"
print "Copying media files to " + target_media_dir
shutil.copy2(template_media_dir + "background.png",target_media_dir)
shutil.copy2(template_media_dir + "logo.png",target_media_dir)
print "Media files copied to " + target_media_dir + "\n"

#set permissions

#run the program

#print next steps

print "finishing"
subprocess.call(["python",project_name + ".py"], cwd=project_name + "/python/")

sys.exit(0)


