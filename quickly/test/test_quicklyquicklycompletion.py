import os
import nose
import subprocess
import shutil

INSIDE_PROJECT = 'add commands configure debug design edit getstarted help license package quickly release run save share submitubuntu test tutorial upgrade'
OUTSIDE_PROJECT = 'commands create getstarted help quickly tutorial'

COMPLETION_DATA = [
[['quickly', "shell-completion", 'quickly', ''], '/tmp', OUTSIDE_PROJECT],
[['quickly', "shell-completion", 'quickly', ''], '/tmp/bar', INSIDE_PROJECT],
[['quickly', "shell-completion", 'quickly', ''], '/tmp/baz', INSIDE_PROJECT],
]

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

def create_mock_project(project, template):
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

    create_mock_project('bar', 'ubuntu-application')
    create_mock_project('baz', 'foo')

def test_setup():
    # sanity check that quickly reacts to mock projects
    for cmdlist, cwd, expected in COMPLETION_DATA: 
        yield assert_setup, cmdlist, cwd, expected

def assert_setup(cmdlist, cwd,  expected):
    stdout, stderr = run(cmdlist, cwd)
    assert expected in stdout, stdout

# now for the real tests
def test_same_child_and_parent_completion():
    for project_command in INSIDE_PROJECT.split(' '):
        yield assert_same_child_and_parent_completion, project_command
        
def assert_same_child_and_parent_completion(project_command):
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
