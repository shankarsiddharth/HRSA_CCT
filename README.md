# hrsaCCT (HRSA Content Creation Tool)

To Freeze the package requirements:
-----------------------------------

pip3 freeze > requirements.txt
To Create the exe using pyinstaller:
------------------------------------

- Creates folders build, dist, <script_name>.spec (eg. main.spec)
- Copy the auth file from Google cloud / embed the auth data in the python scripts
- Copy the Inklecate Windows exe to the output folder
- To Package the data files into the exe:
  https://stackoverflow.com/questions/42100198/include-a-json-file-with-exe-pyinstaller

OneFile / single .exe:
----------------------

`pyinstaller --onefile --windowed __main__.py`

OneDirectory / single .exe:
---------------------------

`pyinstaller --onedir --windowed __main__.py`

Inno Setup Compiler:
--------------------

Sample .iss script => HRSACCT_installer.iss
