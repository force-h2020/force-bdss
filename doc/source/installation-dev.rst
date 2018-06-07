Installation Instructions
-------------------------
To install force-bdss and the workflow manager, first checkout the following
git repositories::

    git clone https://github.com/force-h2020/force-bdss
    git clone https://github.com/force-h2020/force-wfmanager
    git clone https://github.com/force-h2020/force-bdss-plugin-enthought-example

The last repository is optional, but recommended if you want to practice 
writing plugins.

Next, download EDM package manager, and create an appropriate 
environment::

    wget https://package-data.enthought.com/edm/rh5_x86_64/1.9/edm_1.9.2_linux_x86_64.sh && bash ./edm_1.9.2_linux_x86_64.sh -b -f -p $HOME
    export PATH=${HOME}/edm/bin:${PATH}
    edm environments create --version 3.5 force 
    edm shell --environment=force

Verify that your prompt changes to add "(force)".
Install the required packages for the workflow manager::

    cat force-wfmanager/requirements/edm_requirements.txt | grep -v "^#" | while read line; do edm install -y `echo $line | awk '{print $1"=="$2}'`; done

Next, install the required dev packages::

   pip install -r force-wfmanager/requirements/dev_requirements.txt

And the required packages for generating documentation::

   pip install -r force-wfmanager/requirements/doc_requirements.txt

Now, install the bdss::

    pushd force-bdss
    pip install -r requirements/requirements.txt
    pip install -e . 
    popd

the workflow manager::

    pushd force-wfmanager
    pip install -r requirements/requirements.txt
    pip install -e .
    popd

and (optional, but recommended), the example plugins::

    pushd force-bdss-plugin-enthought-example
    pip install -r requirements/requirements.txt
    pip install -e .
    popd

Now you can invoke the workflow manager with force_wfmanager,
and the bdss with force_bdss.
