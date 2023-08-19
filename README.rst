File Generator CLI (FGN)
=========================

FGN is an advanced command-line tool integrating the capabilities of Artificial Intelligence to automate the creation of diverse file types. It's a powerful solution for developers, creatives, managers, or anyone engaged in regular file generation tasks.

FGN leverages the power of OpenAI's GPT models for generating various types of files. This AI integration allows the creation of blogs, code, guides, how-to articles, nano fiction stories, plans, and shell scripts. By merely providing a prompt, you can have a sophisticated AI create meaningful content, saving you time and resources.

Features
--------
- AI-powered file generation with a variety of commands (blog, code, guide, how-to articles, nano fiction stories, plans, and shell scripts)
- Input and output file specification
- Automatic output to file with automatic filename generation
- Clipboard pasting
- Extensible with new commands
- Option for verbose mode for printing output

Installation
------------
FGN is a Python-based command-line tool. Ensure Python and pip are installed on your system. You can install FGN using the following command:

.. code-block:: bash

    pip install fgn

Usage
-----
The FGN tool is used via command line, where you specify a command and the necessary arguments. The general syntax is:

.. code-block:: bash

    fgn [OPTIONS] COMMAND [ARGS]...

Command-line Options
--------------------

.. code-block:: bash

    -m, --model TEXT               The OpenAI model to be used for AGI response.
    -i, --input TEXT               Path to input file.
    -o, --output TEXT              Path to output file.
    -io, --in-n-out TEXT           Path to input and output file.
    -pr, --prompt TEXT             Prompt itself as a string.
    -v, --verbose                  Enable verbose mode for printing output.
    -t, --template TEXT            Path to template file.
    -e, --example TEXT             Path to example file.
    -sp, --system-prompt TEXT      Path to system prompt file.
    -sc, --schema TEXT             Path to response schema definition file.
    --clear-history                Clear the history file.
    -ao, --auto-output             Automatically output to file with automatic file name.
    -as, --auto-summarize INTEGER  Automatic summarization after the specified number of messages.
    -p, --paste                    Paste input from the clipboard.
    -nc, --no-copy                 Do not copy output to the clipboard.
    -tk, --tokens TEXT             Token replacement separated by ;
    -ext, --extension TEXT         File extension of auto output file.
    -d, --dsl TEXT                 Use the FGN Domain Specific Language.
    -a, --append                   Append to the output file.
    --help                         Show this message and exit.

Commands
--------

.. code-block:: bash

  blog      Create a blog article.
  chain     Create chain of fgn commands.
  code      Create a code snippet.
  core      CLI internal usage only.
  dsl       Create a new FGN DSL (requires GPT 4).
  feedback  Create feedback.
  fun       Create OpenAI function schema.
  guide     Create a procedural guide.
  help      Get help with the FGN CLI.
  howto     Create a how-to article.
  lts       Let's think step by step how to do this.
  nano      Create a Nano Fiction story.
  plan      Create a detailed plan.
  prompt    Create a new prompt
  shell     Create a shell script.
  summary   Create a summary.
  template  Create a command named by the prompt.
  yaml      Create yaml.


Examples
--------
Here are some example uses of FGN:

To generate a business plan and save it to "business_plan.txt", run:

.. code-block:: bash

    fgn -o business_plan.txt plan "My Business Plan"

To get a full list of commands and options, run:

.. code-block:: bash

    fgn --help

Key Features
------------
Auto-Output

The auto-output feature is designed to streamline your file creation process. With FGN, you can automatically generate output files using a prompt. The filename is intelligently generated based on the provided prompt, file extensions, and optional parameters. You can control the filename's length, whether to include the current time in the filename, and more. The tool also prevents filename conflicts by generating unique identifiers.

Pasting from Clipboard

FGN supports direct pasting from the clipboard. This feature is particularly useful when you want to generate files based on the data copied to your clipboard. With the '-p' or '--paste' options, you can paste text directly from the clipboard as the command's argument. This feature can significantly speed up your workflow, especially when dealing with large amounts of data.

Extensibility

FGN is designed with extensibility in mind. You can add new commands and functionalities to suit your specific needs. This makes FGN adaptable to a variety of use cases, be it a developer needing to automate code generation or a writer looking to automate blog post creation.
FAQ
---
Answers to frequently asked questions can be found in our FAQ section [link to FAQ section]. If you can't find what you're looking for, feel free to submit an issue through our GitHub page.

Contributing
------------
We welcome your contributions to FGN! Contributions can range from bug fixes, documentation improvements, to proposing new features.

Please refer to our CONTRIBUTING.rst file for more details on how you can contribute to the project.

License
-------
FGN is licensed under the terms of the MIT License. For full details, see the LICENSE file.

Support
-------
For issues or queries about FGN, open a GitHub issue [link to issue tracker]. For additional support, please contact our helpdesk at support@fgn.com.

Making Changes & Contributing
=============================
This project uses `pre-commit`_. Please install it before making any changes:

.. code-block:: bash

    pip install pre-commit
    cd fgn
    pre-commit install

Update the hooks to the latest version:

.. code-block:: bash

    pre-commit autoupdate

Note to contributors: also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====
This project has been set up using PyScaffold 4.5. For details and usage information on PyScaffold see https://pyscaffold.org/.
