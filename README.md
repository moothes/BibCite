# BibCite
BibCite is a visual editor for LaTeX ``.bib`` files.  
Though we currently have a preliminary version with minimal features, we are committed to building a more powerful and user-friendly tool.  
We have a long way to go, and we're excited about the journey ahead.  
Your feedback on our initial version is invaluable as we work to shape the tool's development.  
We welcome any suggestions or contributions, please don't hesitate to contact us at ``csehjzhou@ust.hk``.


## Usage
1. Run ``python main.py``
2. You can select different function as follows:
- Click ``Project -> Open -> BibTex`` to open a ``.bib`` file. You will find that all entries are listed on the left. 
- Click ``Add entry`` button, add a new entry by parsing bibtex (e.g., from Google Scholar) in the new dialog, and save.
- Right click the entry to edit or remove.
- On the Google Scholar Tab, searching by any keyword. Double click or Right click the results can add to the left side.
- On the BibTex Tab, open a another ``.bib`` file, and it will list any new entry. Double click or Right click the results can add to the left side.
5. If you finish editting entries, click ``Export`` button to save to a new ``.bib`` file.  
6. ``data/Prefix.bib`` contains prefix for the saved ``.bib`` file.

## TODO
1. Searching bibtex from Google Scholar
-  We can search on Google Scholar now, but may have some bugs.
2. Adding bibtex from other .bib flie
-  The basic function is OK.
3. Building a template to create .bib file for new paper
4. And more
