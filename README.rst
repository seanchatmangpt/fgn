File Generator CLI (FGN)
=========================

FGN is an AI-assisted command-line file generator with receipt-bound actuation.

Safety and standing
-------------------

FGN separates prompt construction from external consequences. File writes,
clipboard writes, and DSL shell execution route through the broker in
``fgn.core.broker``. The broker writes an admitted JSON receipt before an
operation is attempted and enriches it after consequence observation.
Receipts default to ``~/.fgn/receipts`` and may be relocated with
``FGN_RECEIPT_DIR``.

OpenAI is an optional execution provider. Importing FGN, rendering help, and
deterministic filename generation do not require an API key or the OpenAI SDK.
OpenAI-backed generation requires ``OPENAI_API_KEY`` and emits typed provider
errors when credentials or the SDK are absent.

Installation
------------

.. code-block:: bash

   python -m pip install .
   fgn --help

Development verification
------------------------

.. code-block:: bash

   python -m pip install -e '.[testing]'
   pytest -q tests/test_cli.py tests/test_llm_operations.py
