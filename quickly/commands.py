# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
#
# This file is part of Quickly
#
#This program is free software: you can redistribute it and/or modify it
#under the terms of the GNU General Public License version 3, as published
#by the Free Software Foundation.

#This program is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranties of
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#PURPOSE.  See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along
#with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess
import sys

import builtincommands
import tools

import gettext
from gettext import gettext as _


gettext.textdomain('quickly')

# XXX: What does this comment mean? -- jml, 2009-11-18
# double depths tabular : template (or "builtin"), name
__commands = {}


def get_all_commands():
    """Load all commands

    First, load template command and then builtins one. Push right parameters
    depending if hooks are available, or if the command execution is special
    You can note that create command is automatically overloaded atm.
    """

    if len(__commands) > 0:
        return __commands

    try:
        template_directories = tools.get_template_directories()
    except tools.template_path_not_found:
        template_directories = []
    for template_dir in template_directories:
        for template in os.listdir(template_dir):
            __commands[template] = {}
            template_path = os.path.join(template_dir, template)

            # load special attributes declared for every command
            launch_inside_project_command_list = []
            launch_outside_project_command_list = []
            command_followed_by_command_list = []
            try:
                files_command_parameters = file(
                    os.path.join(template_path, "commandsconfig"), 'rb')
                for line in files_command_parameters:
                    # Suppress commentary after the value in configuration
                    # file and in full line.
                    fields = line.split('#')[0]
                    fields = fields.split('=') # Separate variable from value
                    # normally, we have two fields in "fields"
                    if len(fields) == 2:
                        targeted_property = fields[0].strip()
                        command_list = [
                            command.strip()
                            for command in fields[1].split(';')]
                        if (targeted_property
                            == 'COMMANDS_LAUNCHED_IN_OR_OUTSIDE_PROJECT'):
                            launch_inside_project_command_list.extend(
                                command_list)
                            launch_outside_project_command_list.extend(
                                command_list)
                        if (targeted_property
                            == 'COMMANDS_LAUNCHED_OUTSIDE_PROJECT_ONLY'):
                            launch_outside_project_command_list.extend(
                                command_list)
                        if targeted_property == 'COMMANDS_FOLLOWED_BY_COMMAND':
                            command_followed_by_command_list.extend(
                                command_list)
            except (OSError, IOError):
                pass

            for command_name in os.listdir(template_path):
                file_path = os.path.join(template_path, command_name)
                # if there is a ., remove extension
                if "." in command_name:
                    command_name = ".".join(command_name.split('.')[0:-1])

                # add the command to the list if is executable
                # XXX: It's generally a bad idea to check if you can read to a
                # file. Instead, you should just read it. The file might
                # become unreadable between here and when you actually read
                # it.
                if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                    hooks = {'pre': None, 'post': None}
                    for event in ('pre', 'post'):
                        # XXX: hasattr is evil. Use getattr.
                        event_hook = getattr(
                            builtincommands, event + '_' + command_name, None)
                        if event_hook is not None:
                            hooks[event] = event_hook

                    # define special options for command
                    launch_inside_project = False
                    launch_outside_project = False
                    followed_by_template = False
                    followed_by_command = False
                    if command_name in launch_inside_project_command_list:
                        launch_inside_project = True
                    if command_name in launch_outside_project_command_list:
                        launch_outside_project = True
                        followed_by_template = True
                    if command_name in builtincommands.followed_by_command:
                        followed_by_command = True
                    # default for commands: if not inside nor outside, and
                    # it's a template command, make it launch inside a project
                    # only
                    if not (launch_inside_project or launch_outside_project):
                        launch_inside_project = True

                    __commands[template][command_name] = Command(
                        command_name, file_path, template,
                        launch_inside_project, launch_outside_project,
                        followed_by_template, followed_by_command,
                        hooks['pre'], hooks['post'])


    # add builtin commands (avoiding gettext and hooks)
    __commands['builtins'] = {}
    for elem in dir(builtincommands):
        command = getattr(builtincommands, elem)
        if (callable(command)
            and not command.__name__.startswith(('pre_', 'post_', 'gettext'))):
            command_name = command.__name__
            # here, special case for some commands
            launch_inside_project = False
            launch_outside_project = False
            followed_by_template = False
            followed_by_command = False

            if command_name in builtincommands.launched_inside_project_only:
                launch_inside_project = True
            if command_name in builtincommands.launched_outside_project_only:
                launch_outside_project = True
            if command_name in builtincommands.followed_by_template:
                followed_by_template = True
            if command_name in builtincommands.followed_by_command:
                followed_by_command = True

            # default for commands: if not inside nor outside only, and it's a
            # builtin command, make it launch wherever
            if not launch_inside_project and not launch_outside_project:
                launch_inside_project = True
                launch_outside_project = True

            hooks = {'pre': None, 'post': None}
            for event in ('pre', 'post'):
                if hasattr(builtincommands, event + '_' + command_name):
                    hooks[event] = getattr(
                        builtincommands, event + '_' + command_name)

            __commands['builtins'][command_name] = Command(
                command_name, command, None, launch_inside_project,
                launch_outside_project, followed_by_template,
                followed_by_command, hooks['pre'], hooks['post'])

    return __commands


# XXX: This really ought to be get_commands_by_criteria to be correct grammar,
# if it can return multiple commands. -- jml, 2009-11-18
def get_command_by_criteria(**criterias):
    """Get a list of all commands corresponding to criterias

    Criterias correponds to Command object properties.
    """

    # all criterias are None by default, which means, don't care about the
    # value.
    matched_commands = []
    all_commands = get_all_commands()

    for template_available in all_commands:
        if ('template' in criterias
            and criterias['template'] != template_available):
            # XXX: I'm sure this speeds up the search, but what exactly is it
            # that we're skipping and why is it ok to skip this? -- jml,
            # 2009-11-18.
            continue # to speed up the search
        for candidate_command_name in all_commands[template_available]:
            candidate_command = all_commands[
                template_available][candidate_command_name]
            command_ok = True
            # check all criterias (template has already been checked)
            for elem in criterias:
                if (elem is not 'template'
                    and getattr(candidate_command, elem) != criterias[elem]):
                    command_ok = False
                    continue # no need to check other criterias
            if command_ok:
                matched_commands.append(candidate_command)

    return matched_commands


def get_command_names_by_criteria(**criteria):
    """Get a list of all command names corresponding to criteria.

    'criteria' correponds to Command object properties.
    """
    return (command.name for command in get_command_by_criteria(**criteria))


def get_all_templates():
    """Get a list of all templates"""
    return [
        template for template in get_all_commands().keys()
        if template != "builtins"]


class Command:

    def _die(self, function_name, return_code):
            print _("ERROR: %s command failed") % function_name
            print _("Aborting")
            sys.exit(return_code)

    def __init__(self, command_name, command, template=None,
                 inside_project=True, outside_project=False,
                 followed_by_template=False, followed_by_command=False,
                 prehook=None, posthook=None):
        self.command = command
        self.template = template
        self.prehook = prehook
        self.posthook = posthook
        self.inside_project = inside_project
        self.outside_project = outside_project
        self.followed_by_template = followed_by_template
        self.followed_by_command = followed_by_command
        self.name = command_name

    def shell_completion(self, template_in_cli, args):
        """Smart completion of a command

        This command try to see if the command is followed by a template and
        present template if it's the case. Otherwise, it calls the
        corresponding command argument.
        """

        completion = []

        if len(args) == 1:
            if not template_in_cli:
                if self.followed_by_template: # template completion
                    if not self.template: # builtins command case
                        completion.extend(get_all_templates())
                    else:
                        # complete with current template (which != from
                        # template_in_cli: ex create command (multiple
                        # templates))
                        completion.extend([self.template])
            else: # there is a template, add template commands
                if self.followed_by_command: # template command completion
                    completion.extend(
                        get_command_names_by_criteria(
                            template=template_in_cli))
            if self.followed_by_command: # builtin command completion
                completion.extend(
                    get_command_names_by_criteria(template="builtins"))

        elif len(args) == 2:
            if not template_in_cli and self.followed_by_template:
                template_in_cli = args[0]
                # template command completion and builtins command.
                if self.followed_by_command:
                    completion.extend(
                        get_command_names_by_criteria(
                            template=template_in_cli))
                    completion.extend(
                        get_command_names_by_criteria(template="builtins"))

        # give to the command the opportunity of giving some shell-completion
        # features
        if template_in_cli == self.template and len(completion) == 0:
            if callable(self.command): # Internal function
                completion.extend(
                    self.command(template_in_cli, "", args, True))
            else: # External command
                instance = subprocess.Popen(
                    [self.command, "shell-completion"] + args,
                    stdout=subprocess.PIPE)
                command_return_completion, err = instance.communicate()
                if instance.returncode != 0:
                    print err
                    sys.exit(1)
                completion.extend(command_return_completion.split(','))

        return " ".join(completion)

    def help(self, dest_path, command_args):
        """Print help of the current command"""

        return_code = 0
        if callable(self.command): # intern function, return __doc__
            print (self.command.__doc__)
        else: # launch command with "help" parameter
            return_code = subprocess.call(
                [self.command, "help"] + command_args, cwd=dest_path)

        return return_code

    def is_right_context(self, dest_path, verbose=True):
        """Check if we are in the right context for launching the command"""

        # verbose à false pour l'introspection des commandes dispos

        # check if dest_path check outside or inside only project :)
        if self.inside_project and not self.outside_project:
            try:
                project_path = tools.get_root_project_path(dest_path)
            except tools.project_path_not_found:
                if verbose:
                    print (_(
                        "ERROR: Can't find project in %s.\nEnsure you launch "
                        "this command from a quickly project directory.")
                           % dest_path)
                    print _("Aborting")
                return False
        if self.outside_project and not self.inside_project:
            try:
                project_path = tools.get_root_project_path(dest_path)
                if verbose:
                    # XXX: I don't know about i18n, but shouldn't the
                    # project_path and command be substituted _after_ the
                    # gettext? -- jml, 2009-11-18
                    print _(
                        "ERROR: %s is a project. You can't launch %s command "
                        "within a project. Please choose another path."
                        % (project_path, self.command))
                    print _("Aborting")
                return False
            except tools.project_path_not_found:
                pass

        return True

    def launch(self, current_dir, command_args, template=None):
        """Launch command and hooks for it

        This command will perform the right action (insider function or script
        execution) after having checked the context.
        """

        # template is current template (it will be useful for builtin
        # commands)

        # if template not specified, take the one for the command the template
        # argument is useful when builtin commands which behavior take into
        # account the template name
        if template is None:
            # (which can be None if it's a builtin command launched outside a
            # project)
            template = self.template

        if not self.is_right_context(current_dir): # check in verbose mode
            return 1

        # get root project dir
        try:
            project_path = tools.get_root_project_path(current_dir)
        except tools.project_path_not_found:
            # launch in current project
            project_path = current_dir

        # transition if needed
        if self.inside_project and self.name != "upgrade":
            try:
                get_all_commands()[self.template]['upgrade'].launch(
                    current_dir, [], template)
            except KeyError: # if KeyError, no upgrade command.
                pass

        if self.prehook:
            return_code = self.prehook(template, project_path, command_args)
            if return_code != 0:
                self._die(self.prehook.__name__, return_code)

        if callable(self.command): # Internal function
            return_code = self.command(template, project_path, command_args)
        else: # External command
            return_code = subprocess.call(
                [self.command] + command_args, cwd=project_path)
        if return_code != 0:
            self._die(self.name, return_code)

        if self.posthook:
            return_code = self.posthook(template, project_path, command_args)
            if return_code != 0:
                self._die(self.posthook.__name__, return_code)

        return 0
