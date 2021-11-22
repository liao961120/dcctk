.. dcctk documentation master file, created by
   sphinx-quickstart on Tue Oct 12 10:52:33 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Hanzi Corpus Toolkit
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :numbered:

   query
   stats
   corpusReader
   concordance
   sense


Installation
------------

.. code-block:: bash

   pip install -U hctk


Jupter Notebooks (Colab)
------------------------

In order to work properly on Google Colab, some additional settings (e.g., 
Chinese fonts, interactive visualizing package setup) need to be done:


.. code-block:: bash
   :caption: Display Chinese characters in plot outputs

   # Download font data
   !wget 'https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKtc-hinted.zip'
   !mkdir /tmp/fonts
   !unzip -o NotoSansCJKtc-hinted.zip -d /tmp/fonts/
   !mv /tmp/fonts/NotoSansMonoCJKtc-Regular.otf /usr/share/fonts/truetype/NotoSansMonoCJKtc-Regular.otf -f
   !rm -rf /tmp/fonts
   !rm NotoSansCJKtc-hinted.zip


.. code-block:: python

   # Set chinese font for plotting
   import matplotlib.font_manager as font_manager
   import matplotlib.pyplot as plt

   font_dirs = ['/usr/share/fonts/truetype/']
   font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
   for font_file in font_files:
      font_manager.fontManager.addfont(font_file)
   plt.rcParams['font.family'] = "Noto Sans Mono CJK TC"

.. code-block:: python
   :caption: Setup interactive visualization display

   from bokeh.io import output_notebook
   from bokeh.resources import INLINE
   output_notebook(resources=INLINE)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
