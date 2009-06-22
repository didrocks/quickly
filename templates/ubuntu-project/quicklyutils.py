import string 


def quickly_name(project_name):
    project_name = project_name.lower()
    permitted_characters = string.ascii_lowercase
    permitted_characters += "_"
    for c in project_name:
        if c not in permitted_characters:
            print _("""
ERROR: unpermitted character in project name.
Letters and underscore ("_") only.""")
            sys.exit(0)
    return project_name

def conventional_names(project_name):
    words = project_name.split("_")
    sentence_name = project_name.replace("_"," ")
    sentence_name = string.capwords(sentence_name)
    camel_case_name = sentence_name.replace(" ","")
    return sentence_name, camel_case_name

def file_from_template(template_dir, template_file, target_dir, substitutions, rename = True):
    target_file = template_file
    if rename:
        for s in substitutions:
            pattern, sub = s
            target_file = target_file.replace(pattern,sub)

    print "Creating %s" % target_dir + "/" + target_file
    fin = open(template_dir + template_file,'r')
    file_contents = fin.read()
    for s in substitutions:
        pattern, sub = s
        file_contents = file_contents.replace(pattern,sub)

    fout = open(target_dir + target_file, 'w')
    fout.write(file_contents)
    fout.flush()
    fout.close()
    fout.close()
    print "%s created\n" % (target_dir + "/" + target_file,)

