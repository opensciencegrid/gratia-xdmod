

from distutils.core import setup

setup(name="gratia-xdmod",
      version="0.1",
      author="Mats Rynge",
      author_email="rynge@isi.edu",
      url="https://github.com/opensciencegrid/gratia-xdmod",
      description="Probe for synchronizing Gratia and XDMoD",
      package_dir={"": "src"},
      packages=["gratia_xdmod"],

      scripts = ['src/gratia-xdmod'],

      data_files=[("/etc/cron.d", ["config/gratia-xdmod.cron"]),
            ("/etc/", ["config/gratia-xdmod.cfg"]),
          ],

     )

