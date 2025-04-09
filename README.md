# nbpandoc: Pandoc Jupyter Notebook Convert Tool

## Explainiations

Imagine this: When you want to convert a Markdown file to a PDF via LaTeX with specific formatting requirements using pandoc, you typically use the following command:

```bash
pandoc <filename>.md --output=<filename>.pdf
```

However, this process becomes particularly challenging with Jupyter Notebook files. When attempting this conversion, you may encounter numerous issues. I've compiled the potential problems as follows:

1. The `pandoc` command cannot recognize Jupyter Notebook's first-level heading as the document title. Even with `--shift-heading-level-by=-1`, the generated PDF's title remains empty, requiring additional `--title` parameter specification.
2. Pandoc doesn't read metadata information from Jupyter Notebook's JSON metadata (such as `author`, `date`, or automatic section numbering via `"numbersections": true`). These must be specified through command-line parameters, resulting in verbose commands[^1].
3. When Chinese characters are present in Jupyter Notebooks, you need to use the `ctexart` document class and specify XeLaTeX as the compilation engine. This requires first exporting to plain TeX, manually editing the exported text to modify document classes and add necessary packages.
4. Different Jupyter Notebook files require re-specifying these parameters each
5. time, creating significant redundant work.

You might ask: Why not use Jupyter NBConvert? Well, this might sound offensive, but the truth is: Jupyter NBConvert can be quite difficult for some users. Specifically:

1. It doesn't support directly specifying existing LaTeX document classes for PDF exports, instead requiring users to write JinJa2 templates (NBConvert doesn't support other formats like `*.cls` templates), meaning users must invest extra time learning JinJa2.
2. There's virtually no existing gallery for downloadable NBConvert templates, forcing users to either spend considerable time learning template writing or struggling to find usable ones.
3. If maintaining a personal LaTeX template (like myself), you must simultaneously maintain a JinJa2 template for Jupyter exports.

To address these challenges, I developed this Python command-line utility to convert Jupyter Notebooks into other formats.

## Features

Theoretically, this program `nbpandoc` defaults to PDF via LaTeX conversion, but actually reserves additional interfaces for users to specify other output formats (Such as `*.docx`).

Additionally, it can accept Markdown input similar to my previous project [`panargs`](https://github.com/GitHubonline1396529/panargs), though **this feature remains untested so far**.

## Usage

To convert a Jupyter Notebook file into PDF, you can use:

```bash
nbpandoc <filename>.ipynb
```

> [!warning]
>
> Before running the command, make sure that Pandoc is correctly installed and 
> included in your system's `PATH`. You can verify this by running:
>
> ```bash
> pandoc --version
> ```
>
> If Pandoc is not installed, refer to the official Pandoc documentation for 
> [installation instructions](https://pandoc.org/installing.html).

Flags of `pandoc` command can be assigned in the metadata of the Notebook or with the command-line option `--flag`. See the document for more details.

> [!note]
>
> The `--help` option can be used to display a list of available commands 
> and their descriptions.
>  
> ```txt
> usage: nbpandoc.exe [-h] [--flags FLAGS] filename
> 
> Convert a Markdown or Jupyter notebook file to PDF via Pandoc, including
> full notebook metadata and custom pandoc_args.
> 
> positional arguments:
>   filename       The input file to convert (.md or .ipynb).
> 
> optional arguments:
>   -h, --help     show this help message and exit
>   --flags FLAGS  Extra Pandoc flags (default: --pdf-engine=xelatex).
> ```

## Demos

See [`example/intro.ipynb`](example/intro.ipynb) and [`example/intro.pdf`](example/intro.pdf) as a demo.

> [!caution]
> 
> The ``intro.ipynb`` file is migrated from JupyterLite, licensed under the terms of the BSD 3-Clause License. Please ensure compliance with the license terms when using or distributing this file. 
>
> The original version of this file include some Emoji characters, I removed them for converting this file to PDF via LaTeX. You can clicking [this link](https://github.com/jupyterlite/jupyterlite/blob/main/examples/intro.ipynb>) to visit the original file.

## License

This script is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for more details.

[^1]: For Markdown files, this information can be specified in YAML headers.
