# opensource code snippets and software  
contributor/producer  
IRC: #gentoo < maolang >  
I really need to fill this out with more info, i am slack!  

### matrix_DM_prettifier.py  
download this or git it  
in element (all i know for sure works) go into a DM and:  
room info -> export chat > (*)HTML FROM THE BEGINNING size limit 1999MB (max is 2000MB)  
extract that somewhere and put this script in there (idk where you put it if you wanna type the full path that's on you), cd into that folder on the command line, and do this  
#assuming you're already in the folder with the script and all the html files and other junk element dumped:  
```sh
python3 -m venv .
source bin/activate
pip install bs4
python3 matrix_DM_prettifier.py messages.html # for example...
```  

chatgpt assures me that the following bash script will run this on every html file in the folder and it appears to:
```bash
#!/bin/bash
for file in ./*.html; do
  python3 matrix_DM_prettifier.py "$file"
done
```
