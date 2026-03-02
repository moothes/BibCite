# BibCite
BibCite is a visual editor for LaTeX ``.bib`` files.  
Though we currently have a preliminary version with minimal features, we are committed to building a more powerful and user-friendly tool.  
We have a long way to go, and we're excited about the journey ahead.  
Your feedback on our initial version is invaluable as we work to shape the tool's development.  
We welcome any suggestions or contributions, please don't hesitate to contact us at ``csehjzhou@ust.hk``.


## Usage
1. Run ``python main.py``
2. You can select different functions as follows:
- Click ``Project -> New project`` to create an empty project. Or click ``Project -> Template`` to open an existing ``.bib`` file, and you will find that all entries are listed on the left.
- Click ``New entry`` button. A new dialog will be shown and you need to parses bibtex (e.g., from Google Scholar) and click save.
- Right click the entry to edit or remove.
- In the ``Google Scholar`` Tab, searching by any keyword. Double click or Right click the results can add to the left side.
- In the ``BibTex`` Tab, open another ``.bib`` file, and it will list any new entry. Double click or Right click the results can add to the left side.
- In the ``Storage`` Tab, all entries that you have ever used are stored. Double click or Right click the results can add to the left side.
3. If you finish editting entries, click ``Export`` button to save to a new ``.bib`` file.  
4. ``data/Prefix.bib`` contains prefix for the saved ``.bib`` file.

## TODO
1. Searching on Google Scholar may need to use another threads.
2. Searching on storage by keyworks.
3. And more
