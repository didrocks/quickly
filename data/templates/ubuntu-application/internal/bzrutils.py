
from subprocess import Popen, PIPE

def is_file_versioned(v_file):
    process = Popen(["bzr","status","--short",v_file], stdout=PIPE, stderr=PIPE).communicate()
    output = process[0]
    err = process[1]
    return len(err) == 0 and (len(output) == 0 or not output[0] == '?')
