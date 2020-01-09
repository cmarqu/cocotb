:orphan:

Release Notes
=============

We are using `towncrier <https://pypi.org/project/towncrier/>`_ to handle
our release notes, and this directory contains the input for it -
"news fragments" which are short files that contain a small
**ReST**-formatted text that will be added to the next version's
Release Notes page.

Each file should be named like ``<PULL REQUEST>.<TYPE>.rst``, where
``<PULL REQUEST>`` is a pull request number, and ``<TYPE>`` is one of:

* ``feature``: New user-facing feature.
* ``bugfix``: A bug fix.
* ``doc``: Documentation improvement.
* ``removal``: Deprecation or removal of public API.
* ``misc``: A ticket has been closed, but it is not of interest to users.

.. comment_numpy_has_these:
    * ``new_function``: New user facing functions.
    * ``deprecation``: Changes existing code to emit a DeprecationWarning.
    * ``future``: Changes existing code to emit a FutureWarning.
    * ``expired``: Removal of a deprecated part of the API.
    * ``compatibility``: A change which requires users to change code and is not
      backwards compatible. (Not to be used for removal of deprecated features.)
    * ``c_api``: Changes in the Numpy C-API exported functions
    * ``new_feature``: New user facing features like ``kwargs``.
    * ``improvement``: Performance and edge-case changes
    * ``change``: Other changes
    * ``highlight``: Adds a highlight bullet point to use as a possibly highlight
      of the release.

In that file, make sure to use full sentences with correct case and punctuation,
and do not use a bullet point at the beginning of the file.
Use Sphinx references
(see https://sphinx-tutorial.readthedocs.io/cheatsheet/) if you refer
to added classes, methods etc.

An example line could be ``Summary of new feature.``.

You can install ``towncrier`` and run ``towncrier --draft``
if you want to get a preview of how your change will look in the final release
notes.

.. note::

    This README was adapted from the numpy changelog readme which in turn
    took it from pytest under the terms of the MIT licence.
