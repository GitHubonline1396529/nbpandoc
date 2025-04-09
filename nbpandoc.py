"""
Pandoc Jupyter Notebook Convert Tool
====================================

``nbpandoc`` is a command-line utility to convert Markdown or Jupyter notebook 
files to LaTeX PDF via Pandoc, including full notebook metadata. The Project
only contains one script (This script, I mean the one you are now browsing), and
theoretically speaking, you can run this script directly by using

.. code-block:: shell

    python -u nbpandoc.py <filename>.ipynb
    
to convert a Jupyter Notebook to PDF, but I still recomend you run the build,
which is a standalone executable file. You can place it anywhere on 
your PC and include it in your system ``PATH`` to call it flexibly and 
globally.

.. code-block:: shell

    nbpandoc <filename>.ipynb

See the document for more details.
"""

import argparse
import subprocess
import json
import os
import tempfile


def extract_notebook_metadata(filename):
    """
    This function reads a Jupyter notebook file in JSON format and retrieves the 
    metadata section, which typically contains information about the notebook 
    such as its name, authors, and other custom metadata.
        
    Notes
    -----
    
    * The function handles exceptions gracefully and ensures that an empty 
      dictionary is returned in case of any errors (e.g., file not found, 
      invalid JSON format).
    * The metadata section is optional in Jupyter notebooks, so it may not 
      always be present.

    Parameters
    ----------
    filename : str
        Path to the Jupyter notebook file (.ipynb).

    Returns
    -------
    dict
        The metadata dictionary from the notebook. If the metadata section is
        not found or an error occurs during file reading, an empty dictionary is
        returned.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            nb = json.load(f)
        return nb.get("metadata", {}) or {}
    except Exception:
        return {}


def write_metadata_to_file(metadata):
    """
    The function ``write_metadata_to_file`` writes a metadata dictionary to a 
    temporary JSON file for pandoc.

    Parameters
    ----------
    metadata : dict
        The ``metadata`` parameter is a dictionary containing information that 
        needs to be written to a temporary JSON file for use with Pandoc. This 
        metadata could include details such as document title, author, date, and
        any other relevant information needed for document processing. 

    Returns
    -------
    str
        The function ``write_metadata_to_file`` returns the path to the
        temporary metadata file that was created and written with the provided 
        metadata dictionary.
    """
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=".json", mode="w", encoding="utf-8"
    )
    json.dump(metadata, tmp, ensure_ascii=False, indent=2)
    tmp.close()
    return tmp.name


def replace_underscore_with_hyphen(options):        
    """
    Converts dictionary keys from underscore_style to hyphen-style for CLI 
    arguments. This function takes a dictionary where the keys are in 
    underscore_style and returns a new dictionary where the keys are converted 
    to hyphen-style. This is particularly useful for preparing options to be 
    passed as command-line arguments.

    Parameters
    ----------
    options : dict
        A dictionary containing keys in underscore_style.

    Returns
    -------
    dict
        A new dictionary with the keys converted to hyphen-style.
    """
    return {key.replace("_", "-"): value for key, value in options.items()}


def apppend_pandoc_arguments(pandoc_args, command):
    """
    Analyzes and processes the Pandoc arguments provided in the JSON metadata of
    a Jupyter Notebook file and extends the given command list accordingly.

    Parameters
    ----------
    pandoc_args : dict\, str or list
        The Pandoc arguments to be processed. It can be:
        
        * A dictionary where keys are argument names and values are their
          corresponding values.
        * A string containing space-separated Pandoc flags.
        * A list of strings, where each string is a Pandoc flag or argument.
    command : list
        The list of command-line arguments to which the processed Pandoc
        arguments will be appended.

    Returns
    -------
    list
        The updated command list with the processed Pandoc arguments appended.
        If an invalid item is encountered in the ``pandoc_args`` list or if the
        ``pandoc_args`` type is unsupported.

    Raises
    ------
    ValueError
        "Invalid pandoc_args item: {item}" if an item in ``pandoc_args`` is not
        an instance of class or of a subclass thereof.
    """
    # Dict: convert keys and values
    if isinstance(pandoc_args, dict):
        pandoc_args = replace_underscore_with_hyphen(pandoc_args)
        for key, value in pandoc_args.items():
            cli_key = f"--{key}"

            # List value: JSON-style
            if isinstance(value, list):
                command.append(
                    f"{cli_key}={json.dumps(value, ensure_ascii=False)}"
                )
            else:
                command.append(f"{cli_key}={value}")
    # String: split into flags
    elif isinstance(pandoc_args, str):
        command.extend(pandoc_args.split())
    # List of strings: each is a flag
    elif isinstance(pandoc_args, list):
        for item in pandoc_args:
            if isinstance(item, str):
                command.extend(item.split())
            else:
                raise ValueError(f"Invalid pandoc_args item: {item}")

    return command


def convert_to_pdf(filename, flags="--pdf-engine=xelatex"):
    """
    The ``convert_to_pdf`` function converts a Markdown or Jupyter notebook file 
    to PDF using Pandoc with customizable flags based on metadata handling.

    Parameters
    ----------
    filename : str
        The ``filename`` parameter in the ``convert_to_pdf`` function is a
        string that represents the path to the input file. This file can be 
        either a Markdown file (``.md``) or a Jupyter notebook file (``.ipynb``)
    flags : str\, optional
        The ``flags`` parameter in the ``convert_to_pdf`` function is an 
        optional string that allows you to specify extra Pandoc flags to include
        during the conversion process. By default, the ``flags`` parameter is 
        set to ``--pdf-engine=xelatex``, but you can provide additional flags 
        as, defaults to ``--pdf-engine=xelatex`` (optional)
    """

    base, _ = os.path.splitext(filename)

    # Note that finally I decide not to give any presupposed pandoc option, and
    # all the flags should be specified in the ``"pandoc_args"`` flag. This 
    # design can make this script to be more flexible. So I commented the
    # following several lines.

    # output_filename = f"{base}.pdf"

    # Base command
    command = [
        "pandoc",
        filename,
        # "--standalone",
        # "--to=pdf",
        # f"--output={output_filename}",
    ]

    # Include CLI flags
    if flags:
        command.extend(flags.split())

    # If input is a Jupyter notebook, process metadata
    if filename.lower().endswith(".ipynb"):
        metadata = extract_notebook_metadata(filename)
        # Write full metadata to file for Pandoc
        if metadata:
            meta_file = write_metadata_to_file(metadata)
            command.append(f"--metadata-file={meta_file}")

        # Here we're going to test whether ``"output"`` is specified in Jupyter
        # metadata. If not, it will be ``"{base}.pdf"``.
        output_file = metadata.get("output")
        if output_file == None:
            output_file = f"{base}.pdf"
            command.append(f"--to=pdf")
            command.append(f"--output={output_file}")

        # Process custom pandoc_args
        pandoc_args = metadata.get("pandoc_args")
        if pandoc_args:
            command = apppend_pandoc_arguments(pandoc_args, command)

    # Execute the Pandoc command
    try:
        print("Executing command: ", command)
        subprocess.run(command, check=True)
        print(f"Successfully converted {filename} to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")


def main():
    """
    The main function parses command-line arguments and runs the conversion of a
    Markdown or Jupyter notebook file to PDF using Pandoc with custom flags.
    """
    parser = argparse.ArgumentParser(
        description="Convert a Markdown or Jupyter notebook file to PDF via "
        "Pandoc, including full notebook metadata and custom pandoc_args."
    )
    parser.add_argument(
        "filename", help="The input file to convert (.md or .ipynb)."
    )
    parser.add_argument(
        "--flags",
        default="--pdf-engine=xelatex",
        help="Extra Pandoc flags (default: --pdf-engine=xelatex).",
    )
    args = parser.parse_args()

    convert_to_pdf(args.filename, args.flags)


if __name__ == "__main__":
    main()
