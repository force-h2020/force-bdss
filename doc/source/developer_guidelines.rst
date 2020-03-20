FORCE Project Developer Guidelines
==================================

When contributing to the FORCE project, please clone the relevant Git repository and perform all suggested
changes on a new branch (there is no need to fork the repository). Some general guidelines are provided
below.

Continuous Integration
----------------------

The FORCE project uses a TravisCI runner that will build and test any code pushed to a GitHub
repository. These CI checks can also be performed locally whilst developing.

Mandatory Checks
~~~~~~~~~~~~~~~~

#) Contribute unit tests for any fixes or new features using the ``unittest`` library. Each
   module should contain a ``test/`` folder with python files contributing ``unittest.TestCase``
   objects. You can run (from an ``edm`` environment) the following command to perform all
   unit tests within a repository::

      python -m ci test

   All tests must pass in order for a pull request to be accepted.

#) Use Flake8 style guidelines for new code. These can be tested by running::

      python -m ci flake8

   Note: If you enforce stricter style guidelines (such as Black), then this is fine as long as they
   also pass the Flake8 test.

Optional Checks
~~~~~~~~~~~~~~~

4) Some FORCE projects will also build Sphinx documentation as part of the CI. If this is failing
   for any reason, you can run the following command to debug locally::

      python -m ci docs

#) Some FORCE projects have thresholds for code coverage that must be met when contributing
   new code. These will be defined within a ``coverage.yml`` file in the repository top-level
   directory. You can check the coverage by running::

      python -m ci coverage

   Note: when performing this command locally, the final step will attempt to upload the report
   to TravisCI, which will fail unless an appropriate token is set. This is unnecessary to simply
   view the coverage report and can be ignored.

Pull Request Review
-------------------

When the CI tests are passing locally, push the branch to ``origin`` using::

   git push --set-upstream origin <branch-name>

And create a GitHub pull request describing the changes made and the context for doing so. At the
moment we do not have a template for these requests, but typically developers should try to include
a both a 'Summary' section with a brief outline of the context, as well as a 'Changelog' section
with itemized list of key changes made.

Some projects will explicitly require at least one reviewer for a pull request to be merged. However,
we strongly request that ANY code is reviewed before merging.