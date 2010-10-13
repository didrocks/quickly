#!/bin/sh

quickly --help
# Usage:
#     quickly [OPTIONS] command ...
# 
# Options:
#     -t, --template <template>  Template to use if it differs from default
#                                project one
#                                one used to create the project)
#     --staging                  Target launchpad staging server
#     --verbose                  Verbose mode
#     -h, --help                 Show help information
# 
# Commands:
#     create <template> <project-name> (template is mandatory for this command)
#     quickly <template-origin> <template-dest> to create a create derived template
#     getstarted to get some starting hints
# 
# Examples:
#     quickly create ubuntu-application foobar
#     quickly push 'awesome new comment system'
#     quickly -t cool-template push 'awesome new comment system'
