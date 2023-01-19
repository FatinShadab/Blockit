### Blockit
A simple python script that allows you to block or unblock any website on your local machine. The script uses the hosts file to block or unblock websites.

### Requirements
    - Python 3.x
    - os python module
    - socket python module
    - getpass python module
    - fileinput python module
    - typing python module
    - prettytable python module

### Usage
    Run the script using python
    The script will prompt you to enter a command
    The commands are HOME, BLOCK, UNBLOCK, LIST, MASTERPASS, HELP, EXIT 

#### HOME
> Shows the home screen of the script

#### BLOCK
> Prompts you to enter a website to block. It will then block the website by adding an entry to the hosts file.

#### UNBLOCK
> Prompts you to enter a website to unblock. It will then unblock the website by removing the entry from the hosts file.

#### LIST
> Lists all the blocked websites

#### MASTERPASS
> Allows you to set or update the master password. The master password is required to perform certain actions.

#### HELP
> Displays some troubleshoot

#### EXIT
> Exits the script

### Note
    - This script has been developed and tested on Windows.
    - The script uses the hosts file located at C:\Windows\System32\drivers\etc\hosts

### License
MIT

This script is for educational and personal use only. Use at your own risk.