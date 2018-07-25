Installation Instructions
-------------------------
To install force-bdss and the workflow manager, first checkout the following
git repositories::

    git clone https://github.com/force-h2020/force-bdss
    git clone https://github.com/force-h2020/force-wfmanager
    git clone https://github.com/force-h2020/force-bdss-plugin-enthought-example

The last repository is optional, but recommended if you want to practice
writing plugins.

Next, download EDM package manager, and create a bootstrap environment::

    wget https://package-data.enthought.com/edm/rh5_x86_64/1.9/edm_1.9.2_linux_x86_64.sh && bash ./edm_1.9.2_linux_x86_64.sh -b -f -p $HOME
    export PATH=${HOME}/edm/bin:${PATH}
    edm environments create --version 3.5 force
    edm install -y -e force-bootstrap click setuptools
    edm shell --environment=force-bootstrap

Verify that your prompt changes to add "(force-bootstrap)".
Installation of the force BDSS runtime environment is performed with the
following command::

    python -m ci build-env

This will create another edm environment called ``force-py27``.

To install the BDSS::

    python -m ci install

To install the workflow manager::

    pushd force-wfmanager
    python -m ci install
    popd

and (optional, but recommended), the example plugins::

    pushd force-bdss-plugin-enthought-example
    python -m ci install
    popd

Now you can enter the deployed environment and invoke the programs::

    edm shell -e force-py27
    # Invokes the workflow manager UI
    force_wfmanager
    # Invokes the CLI BDSS evaluator
    force_bdss

