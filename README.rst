File Generator CLI (FGN)
========================

FGN is an AI-assisted command-line file generator with receipt-bound actuation.

Safety and standing
-------------------

FGN separates parsing and construction from consequences. File writes,
clipboard writes, local model execution, admitted generated-Python execution,
and DSL shell execution route through ``fgn.core.broker``. The broker persists
an admitted JSON receipt before an operation is attempted and enriches it after
consequence observation. Receipts default to ``~/.fgn/receipts`` and may be
relocated with ``FGN_RECEIPT_DIR``.

Generated Python has no ambient execution authority. APIs that compile rendered
classes require ``admitted=True`` and otherwise emit
``REFUSED:PYTHON_AUTHORITY_REQUIRED``. DSL shell execution follows the same law.

Provider boundaries
-------------------

OpenAI and local Llama are optional execution providers. Importing FGN,
rendering templates, generating deterministic filenames, and running ``--help``
do not require either provider. OpenAI-backed generation requires the
``openai`` extra plus ``OPENAI_API_KEY``. Local llama.cpp integration requires
explicit invocation and executes through the broker.

Installation
------------

.. code-block:: bash

   python -m pip install .
   fgn --help

Optional providers and template enhancements:

.. code-block:: bash

   python -m pip install '.[openai]'
   python -m pip install '.[local_llama]'
   python -m pip install '.[template_enhancements]'

Development verification
------------------------

.. code-block:: bash

   python -m pip install -e '.[testing]'
   python -m compileall -q src tests
   pytest -q
   python -m build --sdist --wheel
