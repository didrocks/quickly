import os
import nose
import subprocess
import shutil

COMPLETION_DATA = [
[['quickly', "shell-completion", 'quickly', ''], '/tmp', 'commands create getstarted help quickly tutorial'],
[['quickly', "shell-completion", 'quickly', ''], '/tmp/bar', 'add commands configure debug design edit getstarted help license package quickly release run save share submitubuntu test tutorial upgrade'],
[['quickly', "shell-completion", 'quickly', ''], '/tmp/baz', 'add commands configure debug design edit getstarted help license package quickly release run save share submitubuntu test tutorial upgrade'],
]

COUNT_PROJECT_COMMANDS = 19

def run(cmdlist, cwd='/tmp'):
    my_env = os.environ.copy()
    my_env["HOME"] = "/tmp" # our test template goes here

    instance = subprocess.Popen(
                cmdlist,
                cwd=cwd,
                env=my_env, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    stdout, stderr = instance.communicate()
    return stdout, stderr

def setup_project(project, template):
    # use a mock project because it is quicker
    path = os.path.join('/tmp', project)
    os.makedirs(path)

    filename = path = os.path.join(path, '.quickly')
    with open(filename, 'w') as f:
        f.write('project = %s\n' % project)
        f.write('version = any\n')
        f.write('template = %s\n' % template)

def setup():
    # setup for module automatically called once before tests
    shutil.rmtree('/tmp/quickly-templates', True)
    shutil.rmtree('/tmp/bar', True)
    shutil.rmtree('/tmp/baz', True)
    
    # setup template
    stdout, stderr = run(['quickly', 'quickly', 'ubuntu-application', 'foo'])
    assert 'foo template from ubuntu-application' in stdout, stdout

    setup_project('bar', 'ubuntu-application')
    setup_project('baz', 'foo')

def test_command_list_completion():
    # sanity check that quickly reacts to mock projects
    for cmdlist, cwd, expected in COMPLETION_DATA: 
        yield ensure_command_list_completion, cmdlist, cwd, expected

def ensure_command_list_completion(cmdlist, cwd,  expected):
    stdout, stderr = run(cmdlist, cwd)
    assert expected in stdout, stdout

def test_same_child_and_parent_completion():
    cmdlist = ['quickly', "shell-completion", 'quickly', '']
    parent_path = '/tmp/bar'
    parent_stdout, stderr = run(cmdlist, parent_path)
    str_project_commands = parent_stdout.split('\n')[0]
    # these fail with version 11.10
    # add configure license

    list_project_commands = str_project_commands.split(' ')

    # a simple sanity check
    assert len(list_project_commands) == COUNT_PROJECT_COMMANDS

    for project_command in list_project_commands:
        yield ensure_same_child_and_parent_completion, project_command
        
def ensure_same_child_and_parent_completion(project_command):
    cmdlist = ['quickly', "shell-completion", 'quickly', project_command, '']
    parent_path = '/tmp/bar'
    child_path = '/tmp/baz'
    parent_stdout, stderr = run(cmdlist, parent_path)
    assert stderr == ''
    child_stdout, stderr = run(cmdlist, child_path)
    assert stderr == ''
    
    assert parent_stdout == child_stdout, child_stdout

if __name__ == '__main__':    
    nose.runmodule()
