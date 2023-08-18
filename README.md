# Splive <!-- omit in toc -->

[![PyPI - Version](https://img.shields.io/pypi/v/dhlabel?style=flat-square)](https://pypi.org/project/dhlabel/)
[![Repo Version](https://img.shields.io/github/v/tag/chrismettal/dhlabel?label=RepoVersion&style=flat-square)](https://github.com/Chrismettal/DHLabel)
[![PyPI - License](https://img.shields.io/pypi/l/dhlabel?style=flat-square)](https://pypi.org/project/dhlabel/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dhlabel?style=flat-square)](https://pypi.org/project/dhlabel/)
[![Donations: Coffee](https://img.shields.io/badge/donations-Coffee-brown?style=flat-square)](https://github.com/Chrismettal#donations)

This is a work in progress.

For some reason, DHL exported labels print over the entire A4 page, wasting half of your self sticking labels. Additionally, for international orders, an entire second A4 label is used for the CN22/CN23 document.

This tool grabs these two pages, deletes the half of the page that isn't required for anything, and puts both the label and CN22 on the same page for printing. Additionally, it will fill out the current date into the CN22/CN23 date field so you only need to sign it.

**If you like my work please consider [supporting me](https://github.com/Chrismettal#donations)!**

## Installation

### Pypi

Might be pushed to Pypi later idk.

### Local (for development)

- Clone the repo:

`git clone https://github.com/chrismettal/dhlabel`

- Change directory into said cloned repo:

`cd dhlabel`

- Install in "editable" mode:

`pip install -e .`

## Usage

Execute `dhlabel` in the folder containing your downloaded labels fresh from DHL. Alternatively, specify the target path after the command like `dhlabel /path/to/source/pdfs`.

It should automatically detect national and international orders based on the number of pages in the original document and attempt to use as little pages as possible for your orders (First dumping each international order into one PDF page, before using half a page per national order)

2 files, `DHLabel_YYYY-MM-DD.pdf` and `DHLabel_YY-MM-DD.csv` will be created after completion, where the PDF contains all your labels in one file, and the CSV is a list of recipients and their tracking numbers.


## Roadmap

- [x] Consolidate international labels into one page
- [ ] Consolidate 2 national labels into one page
- [x] Find list of files
  - [ ] Detect national vs international order
- [x] Append multiple orders into the same file

## Donations

**If you like my work please consider [supporting my caffeine addiction](https://gitlab.com/Chrismettal#donations)!**

## License

 <a rel="GPLlicense" href="https://www.gnu.org/licenses/gpl-3.0.html"><img alt="GPLv3" style="border-width:0" src="https://www.gnu.org/graphics/gplv3-or-later.png" /></a><br />This work is licensed under a <a rel="GPLlicense" href="https://www.gnu.org/licenses/gpl-3.0.html">GNU GPLv3 License</a>.
