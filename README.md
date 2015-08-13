This script is meant to synchronize and summarize job records from the OSG
Gratia system into XDMoD system.

To make a release:
  - Update versions in config/gratia-xdmod.spec and setup.py
  - Update the changelog in the spec file.
  - Run "python setup.py sdist" to generate the source tarball in dist/
  - Copy the source tarball into ~/rpmbuild/SOURCES
  - Run "rpmbuild -ba config/gratia-xdmod.spec" to create the RPM.
  - Commit changes, tag, and push to github.

