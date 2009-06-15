import os
import sys
import ConfigParser

import gettext
from gettext import gettext as _

config = {}

def check_config_file(config_file_path=None):
    '''Try to guess where the .quickly config file is.
    
    config_file_path is optional (needed by the new command, for instance).
    getcwd() is taken by default.
    
    If nothing found, try to find it up to 4 parent directory
    '''

    if config_file_path is None:
        current_path = os.getcwd()
    else:
        current_path = config_file_path

    for related_directory in ('./', './', '../', '../../', '../../../', '../../../../'):
        quickly_file_path = os.path.abspath(current_path + '/' + related_directory + ".quickly")
        if os.path.isfile(quickly_file_path):
            return quickly_file_path
    return ""
        
    
#project-name=
#template=
#project-lp-id=


def loadConfig():
    """ load configuration from quickly_file_path"""

    # retrieve .quickly file
    quickly_file_path = check_config_file()
    # if no .quickly, create it in cwd
    if not quickly_file_path:
        print _("ERROR: Can't load configuration in current path or its parent ones.")
        return 1    
        
    try:
        fileconfig = file(quickly_file_path, 'rb')
        for line in fileconfig: 
            fields = line.split('#')[0] # Suppress commentary after the value in configuration file and in full line
            fields = fields.split('=') # Separate variable from value
            # normally, we have two fields in "fields"
            if len(fields) == 2:
                config[fields[0].strip()] = fields[1].strip() 
        fileconfig.close()
    except (OSError, IOError), e:
        print _("ERROR: Can't load configuration in %s: %s" % (quickly_file_path, e))
        return 1


def saveConfig(config_file_path=None):
    """ save the configuration file from config dictionnary

    config_file_path is optional (needed by the new command, for instance).
    getcwd() is taken by default.    
    
    keep commentaries and layout from original file """

    # retrieve .quickly file
    quickly_file_path = check_config_file(config_file_path)
    
    # if no .quickly, create it using config_file_path or cwd
    if not quickly_file_path:
        if config_file_path is not None:
            quickly_file_path = os.path.abspath(config_file_path) + '/.quickly'
        else:
            quickly_file_path = os.getcwd() + "/.quickly"
        print _("ERROR: No .quickly file found. Initiate a new one")
    
    try:
        filedest = file(quickly_file_path + '.swp', 'w')
        try:
            fileconfig = file(quickly_file_path, 'rb')
            remaingconfigtosave = config.copy()
            for line in fileconfig:
                fields = line.split('#')[0] # Suppress commentary after the value in configuration file and in full line
                fieldsafter = line.split('#')[1:]
                fields = fields.split('=') # Separate variable from value
                # normally, we have two fields in "fields" and it should be used by config tabular
                if len(fields) == 2 and fields[0].strip() in remaingconfigtosave:
                    line = fields[0].strip() + " = " + remaingconfigtosave.pop(fields[0].strip())
                    if len(fieldsafter) > 0:
                        line = line + " #" + "#".join(fieldsafter) # fieldsafter already contains \n
                    else:
                        line = line + "\n"
                filedest.write(line) # commentaries or empty lines, anything other things which is not useful will be printed unchanged
            # write remaining data if some (new data not in the old config file).
            filedest.write("".join(elem + " = " + remaingconfigtosave[elem] + '\n' for elem in remaingconfigtosave)) #\n here for last element (and not be added, when no iteration to do)
#            print "\n".join(elem + " = " + remaingconfigtosave[elem] for elem in remaingconfigtosave)
            fileconfig.close()
        except (OSError, IOError), e:      
            # write config file from scratch (no previous file found)
            filedest.write("\n".join(elem + " = " + config[elem] for elem in config))
        finally:
            filedest.close()
            os.rename(quickly_file_path + '.swp', quickly_file_path)
    except AttributeError, e:
        print _("ERROR: Can't save configuration in %s" % quickly_file_path)
        return 1
    return 0
    

