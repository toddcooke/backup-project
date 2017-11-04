# Atlas Backup

Atlas Backup is a simple backup program intended for a single user 
on a single computer. The project was created for Vermont Tech's Software Engineering 
CIS 4150 class.

 
![alt text](atlas_backup.png "Atlas Backup screenshot")


#### How to start Atlas Backup:

1. Ensure python 2.7.x is installed
https://www.python.org/downloads/release/python-2712/

2. Ensure a modern web browser (chrome or firefox) is installed
https://www.google.com/chrome/browser/desktop/index.html
https://www.mozilla.org/en-US/firefox/new

3. Start main.py
On linux/mac: `$ python /path/to/main.py`
On windows: click on main.py

4. Go to localhost, port 8080:
[https://127.0.0.1:8080](https://127.0.0.1:8080)

5. To exit, close the terminal window

#### Enabling Recurring Backups:
Since the program can only backup when it is running,
you may want to have this program start up automatically at boot.

On Windows:
https://answers.microsoft.com/en-us/windows/forum/windows_7-windows_programs/how-to-add-a-program-to-startup/91d18255-659e-4796-87f6-5e6c814c7d50

On Mac:
https://stackoverflow.com/questions/6442364/running-script-upon-login-mac

On Linux:
https://stackoverflow.com/questions/12973777/how-to-run-a-shell-script-at-startup


#### Code used:

Bottle Web Framework
http://bottlepy.org/docs/dev/

de/encrypt source
https://gist.github.com/ilogik/6f9431e4588015ecb194

de/compress source
https://stackoverflow.com/questions/8156707/gzip-a-file-in-python
