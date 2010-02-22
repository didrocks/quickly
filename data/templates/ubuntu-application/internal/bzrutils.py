
from subprocess import Popen, PIPE

def is_file_versioned(v_file):
    output = Popen(["bzr","status","--short",v_file], stdout=PIPE, stderr=PIPE).communicate()[0]
    return len(output) > 0 and not output[0] == '?'
