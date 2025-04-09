Building the Executable
-----------------------

If you need to build the executable manually, you can refer to the following 
steps.

Activate the Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, activate the virtual environment using the appropriate command for your 
operating system:

On Windows, if you are using PowerShell:

.. code-block:: powershell

   .venv\Scripts\activate.ps1

If you are using Command Prompt (CMD):

.. code-block:: batch

   .venv\Scripts\activate.bat

On macOS/Linux:

.. code-block:: bash

   source .venv/bin/activate

If a virtual environment does not exist, you may need to create one yourself:

.. code-block:: bash

   python -m venv .venv

.. note::

   It is important to build the executable in the virtual environment. If you 
   build it in your global environment, it may lead to dependency conflicts or
   unexpected behavior.

To exit the virtual environment at any time, you can  simply use `deactivate` 
command:

.. code-block:: bash

   deactivate

Install Required Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~

After activating the virtual environment, install the necessary dependencies:

.. code-block:: bash

   pip install -r requirements.txt

Build the Executable
~~~~~~~~~~~~~~~~~~~~

Finally, use PyInstaller to build the executable:

.. code-block:: bash

   pyinstaller --onefile --clean --name nbpandoc nbpandoc.py

Finally you will find the executable file in `dict` directory.