.. image:: https://raw.githubusercontent.com/molassesapp/molasses-go/main/logo.png
        :width: 100
        :height: 100
        :target: https://molasses.app

===============
molasses-python
===============

.. image:: https://img.shields.io/pypi/v/molasses.svg
        :target: https://pypi.python.org/pypi/molasses


A Python SDK for Molasses. It allows you to evaluate user's status for a feature. It also helps simplify logging events for A/B testing.

Molasses uses polling to check if you have updated features. Once initialized, it takes microseconds to evaluate if a user is active.


Install
-------

.. code:: python

  pip install molasses


Usage
-----

Initialization
~~~~~~~~~~~~~~

Start by initializing the client with an ``APIKey``. This begins the
polling for any feature updates. The updates happen every 15 seconds.

.. code:: python

   from molasses import MolassesClient

   client = MolassesClient("test_key")

If you decide not to track analytics events (experiment started,
experiment success) you can turn them off by setting the ``send_events``
field to ``False``

.. code:: python

   client = MolassesClient("test_key",  send_events=False)

Check if feature is active
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can call ``is_active`` with the key name and optionally a user’s
information. The ``id`` field is used to determine whether a user is
part of a percentage of users. If you have other constraints based on
user params you can pass those in the ``params`` field.

.. code:: python

    client.is_active("FOO_TEST", {
      "id":"foo",
      "params":{
        "isBetaUser":"false",
        "isScaredUser":"false"
       }
    })

You can check if a feature is active for a user who is anonymous by just
calling ``is_active`` with the key. You won’t be able to do percentage
roll outs or track that user’s behavior.

.. code:: python

   client.is_active("TEST_FEATURE_FOR_USER")

Experiments
~~~~~~~~~~~

To track whether an experiment was successful you can call
``experiment_success``. experiment_success takes the feature’s name, any
additional parameters for the event and the user.

.. code:: python

   client.experiment_success("GOOGLE_SSO",{
           "version": "v2.3.0"
       },{
      "id":"foo",
      "params":{
        "isBetaUser":"false",
        "isScaredUser":"false"
       }
    })

Example
-------

.. code:: ruby

   from molasses import MolassesClient

   client = MolassesClient("test_key")

   if client.is_active('NEW_CHECKOUT'):
     print "we are a go"
   else:
     print "we are a no go"

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
