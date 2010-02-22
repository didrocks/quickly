quickly create ubuntu-application test-project
cd test-project
grep LaunchpadIntegration.set_sourcepackagename bin/test-project 
#         LaunchpadIntegration.set_sourcepackagename('test-project')

quickly configure lp-project gpoweroff
grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('gpoweroff')

bzr status
# modified:
#   .quickly
#   bin/test-project
#   data/ui/AboutTestProjectDialog.ui
#   setup.py
# unknown:
#   apport/
#   etc/

bzr add

quickly configure lp-project hudson-notifier
grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('hudson-notifier')

bzr status
# added:
#   apport/
#   apport/source_hudson-notifier.py
#   etc/
#   etc/apport/
#   etc/apport/crashdb.conf.d/
#   etc/apport/crashdb.conf.d/hudson-notifier-crashdb.conf
# modified:
#   .quickly
#   bin/test-project
#   data/ui/AboutTestProjectDialog.ui
#   setup.py

bzr commit -m "Test save"

quickly configure lp-project gpoweroff
grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('gpoweroff')

bzr status
# renamed:
#   apport/source_hudson-notifier.py => apport/source_gpoweroff.py
#   etc/apport/crashdb.conf.d/hudson-notifier-crashdb.conf => etc/apport/crashdb.conf.d/gpoweroff-crashdb.conf
# modified:
#   .quickly
#   bin/test-project
#   data/ui/AboutTestProjectDialog.ui
#   setup.py
#   apport/source_gpoweroff.py
#   etc/apport/crashdb.conf.d/gpoweroff-crashdb.conf

bzr commit -m "Renaming hooks"

rm -rf apport
quickly configure lp-project hudson-notifier
grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('hudson-notifier')

quickly configure lp-project gpoweroff
grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('gpoweroff')

bzr status
#

rm apport/source_gpoweroff.py
quickly configure lp-project hudson-notifier
bzr status
# renamed:
#   apport/source_gpoweroff.py => apport/source_hudson-notifier.py
#   etc/apport/crashdb.conf.d/gpoweroff-crashdb.conf => etc/apport/crashdb.conf.d/hudson-notifier-crashdb.conf
# modified:
#   .quickly
#   bin/test-project
#   data/ui/AboutTestProjectDialog.ui
#   setup.py
#   apport/source_hudson-notifier.py
#   etc/apport/crashdb.conf.d/hudson-notifier-crashdb.conf

bzr commit -m "Prior to upgrade"
quickly upgrade
bzr status
#


rm -rf apport
rm -rf etc
bzr commit -m "Prior to upgrade again"
bzr status
# unknown:
#   apport/
#   etc/
