Installation Instructions
-------------------------
To install force-bdss and the workflow manager, first checkout the following
git repositories::

    git clone https://github.com/force-h2020/force-bdss
    git clone https://github.com/force-h2020/force-wfmanager
    git clone https://github.com/force-h2020/force-bdss-plugin-enthought-example

The last repository is optional, but recommended if you want to practice
writing plugins.

If you never installed the Enthought Deployment Manager, perform the following operations::

    wget https://package-data.enthought.com/edm/rh5_x86_64/1.11/edm_1.11.0_linux_x86_64.sh && bash ./edm_1.11.0_linux_x86_64.sh-b -f -p $HOME
    export PATH=${HOME}/edm/bin:${PATH}
    edm install --version 3.6 -y click setuptools
    edm shell

If you instead already have an EDM installation and a default environment, perform the following:

    edm shell
    edm install -y click setuptools

Verify that your shell prompt now contains the string "(edm)".
You are now in your default EDM environment, and we assume this environment to be the bootstrap environment.
The BDSS software will not be installed in this environment, but in a separate one. The following
commands however must be executed from the bootstrap environment.

Installation of the force BDSS runtime environment is performed with the
following command. This should be done from the directory containing the 'force-bdss' folder::

    pushd force-bdss
    python -m ci build-env

This will create another edm environment called ``force-py36``.
Do not enter this environment. 

To install the BDSS::

    python -m ci install
    popd
    
To install the workflow manager::

    pushd force-wfmanager
    python -m ci install
    popd

and (optional, but recommended), the example plugins::

    pushd force-bdss-plugin-enthought-example
    python -m ci install
    popd

Now you can enter the deployed environment and invoke the programs::

    edm shell -e force-py36
    # Invokes the workflow manager UI
    force_wfmanager
    # Invokes the CLI BDSS evaluator
    force_bdss

