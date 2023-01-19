# REQUIRED IMPORTS FOR THE PROGRAMME
import os
import socket
import getpass
import fileinput
from typing import List
from prettytable import PrettyTable

# SET THE TERMINAL WINDOW TO SPECIFIC SIZE
COLS = 70
ROWS = 45
os.system(f"mode con: cols={COLS} lines={ROWS}")

# CONSTANT VARIABLES FOR THE PROGRAMME
OS_TYPE    : str       = os.name
HOST_FILE  : str       = "C:\Windows\System32\drivers\etc\hosts"
IP         : str       = socket.gethostbyname(socket.gethostname())
WINDOWS  : List[str] = ["HOME", "BLOCK", "UNBLOCK", "LIST", "MASTERPASS", "HELP", "EXIT"]

# ERROR TYPES
PERMISSION_ERROR     = 13
FILE_NOT_FOUND_ERROR =  2

# HEAD LOGO
LOGO = f"""
\t ____    ___                   __          __             
\t/\  _`\ /\_ \                 /\ \      __/\ \__          
\t\ \ \L\ \//\ \     ___     ___\ \ \/'\ /\_\ \ ,_\         
\t \ \  _ <'\ \ \   / __`\  /'___\ \ , < \/\ \ \ \/         
\t  \ \ \L\ \\_\ \_/\ \L\ \/\ \__/\ \ \\`\\ \ \ \ \_        
\t   \ \____//\____\ \____/\ \____\\ \_\ \_\ \_\ \__\       
\t    \/___/ \/____/\/___/  \/____/ \/_/\/_/\/_/\/__/                                                           
"""

# CHECKS FOR MASTERPASS IN THE FILE
def has_masterpass() -> int:
    with open(HOST_FILE, "r+") as hostFile:
        lines = hostFile.readlines()
        if (len(lines) > 21):
            if lines[21].split()[0] == "#MASTERPASS":
                return 1

    return 0

# GET THE MASTERPASS FROM FILE
def get_masterpass() -> str:
    with open(HOST_FILE, "r+") as hostFile:
        return bytes.fromhex(hostFile.readlines()[21].split()[1]).decode('utf-8')
                
# SET THE MASTERPASS IF NOT FOUND IN FILE
def set_masterpass() -> str:
    print()
    print("*** SET MASTERPASS TO CONTINUE ***".center(COLS))
    print()

    masterPass_1 : str = getpass.getpass(prompt='MASTER PASS : ').strip()

    if len(masterPass_1) < 6:
        return "MASTERPASS MUST BE AT LEAST OF LENGTH 6 !"

    masterPass_2 : str = getpass.getpass(prompt='TYPE AGAIN  : ').strip()

    if (masterPass_1 == masterPass_2):
        encoded_pass : str = masterPass_1.encode('utf-8').hex()
        with open(HOST_FILE, "a+") as hostFile:
            hostFile.write(f"#MASTERPASS {encoded_pass}\n")

        return "MASTERPASS REGISTERED SUCCESSFULLY"

    return "DIDN'T MATCH ! TRY AGAIN."

# VALIDATE THE USER INPUT(MASTERPASS)
def valid_masterpass() -> int:
    print()
    userPass : str = getpass.getpass(prompt="ENTER MASTERPASS : ").strip()

    with open(HOST_FILE, "r+") as hostFile:
        if userPass == get_masterpass():
            hostFile.close()
            return 1
        else:
            hostFile.close()
            return 0

# UPDATE THE MASTERPASS
def update_masterpass() -> None:
    print()
    valid_pass : int = 0

    while not valid_pass:
        masterPass_1 : str = getpass.getpass(prompt='NEW MASTERPASS : ').strip()
        masterPass_2 : str = getpass.getpass(prompt='TYPE AGAIN  : ').strip()
        
        if len(masterPass_1) < 6:
            print("MASTERPASS MUST BE AT LEAST OF LENGTH 6 !")
            valid_pass = 0
        else:
            valid_pass = 1

        if masterPass_1 != masterPass_2:
            print("DIDN'T MATCH ! TRY AGAIN.")
            valid_pass = 0
        else:
            valid_pass = 1

    for idx, line in enumerate(fileinput.input(HOST_FILE, inplace=True)):
        if idx == 21:
            print(f"#MASTERPASS {masterPass_1.encode('utf-8').hex()}")
        else:
            print(line.strip())
        

    fileinput.close()
    
    return

# THE WEB IP BLOCKER FUNCTION
def block(website : str) -> int:
    """
        THE WEB IP BLOCKER FUNCTION
        This function takes a website as an input and blocks it by adding the website's IP address to the host file.

        Parameters:
            website (str): The website to be blocked.

        Returns:
            int:
                0   : If the website is already blocked.
                1   : If the website is blocked successfully.
                2   : If "FileNotFoundError" occurs.
                13  : If "PermissionError" occurs.
    """
    block_statement = f"{IP} {website.strip()}\n"

    try:
        with open(HOST_FILE, 'r+') as hostFile:
            if block_statement in hostFile.readlines():
                hostFile.close()
                return 0

        with open(HOST_FILE, 'a+') as hostFile:
            hostFile.write(block_statement)
            hostFile.close()
            return 1 

    except (FileNotFoundError, PermissionError)  as e:
        return e.errno

# THE WEB IP UNBLOCKER FUNCTION
def unblock(website : str) -> int:
    """
        This function is used to unblock a website by removing it from the host file.
 
        Parameters:
            - website (str): The name of the website to unblock.
    
        Returns:
            int: 1 if the website was blocked and unblocked, 0 otherwise.
            int: 2 if "FileNotFoundError" occurs.
            int: 13 if "PermissionError" occurs.
    """
    try:
        web_was_blocked : int = 0
        line_to_remove  : str = f"{IP} {website.strip()}"

        for line in fileinput.input(HOST_FILE, inplace=True):
            if line.strip() != line_to_remove:
                print(line, end="")
            else:
                web_was_blocked = 1

        fileinput.close()

        return web_was_blocked

    except (FileNotFoundError, PermissionError)  as e:
        return e.errno

# THE FUNCTION TO PRINT THE BLOCKED WEB ADDRESS
def show_list() -> None:
    blockTable = PrettyTable()
    blockTable.field_names = ["IP", "WEB"]

    with open(HOST_FILE, 'r+') as hostFile:
        lines = hostFile.readlines()

        if (len(lines) > 22):
            for line in lines[22:]:
                blockTable.add_row([content.strip() for content in line.split()])

            for s in blockTable.get_string().split("\n"):
                print(f"{s}".center(COLS))
        else:
            print("\n\n\n")
            print("<-- EMPTY -->".center(COLS))
            print("\n\n\n")
    return

# THE FUNCTION TO PRINT THE HEADER
def ui(win : str, msg : str) -> None:
    os.system("cls")

    print("="*COLS)
    print(LOGO)
    print("="*COLS)
    print(f"[WIN] {win}".center(COLS))
    print("="*COLS)

    if (win == WINDOWS[0]):
        print("OPTIONS :\t1|BLOCK \t2|UNBLOCK \t3|BLOCK LIST")
        print("\t\t4|MASTERPASS \t5|HELP \t\t6|EXIT")
        print("="*COLS)

    if (win == WINDOWS[4]):
        print("OPTIONS :\t1|SHOW  \t2|UPDATE \t3|RETURN")
        print("="*COLS)

        if (msg):
            print()
            print(f"🔔 {msg}\n".center(COLS))

        op : str = input("Select a option [1/2/3] : ")

        if   (op == '1'):
            if not valid_masterpass():
                return ui(win, f"Invalid MASTERPASS!")

            print()
            print(f"MASTERPASS : {get_masterpass()}".center(COLS))
            input("\nEnter to go to 'HOME' ...")
        elif (op == '2'):
            if not valid_masterpass():
                return ui(win, f"Invalid MASTERPASS!")

            update_masterpass()

            print("\n")
            print("MASTERPASS UPDATED SUCCESSFULLY.".center(COLS))
            print("\n")

            input("\nEnter to go to 'HOME' ...")
            
        elif (op == '3'):
            pass
        else:
            ui(win, f"Invalid Option {op}!")

    if (win == WINDOWS[5]):
        print()
        print("If a website is reachable after adding to the blacklist, check if")
        print("you have given the address correctly example, for facebook it will")
        print("be 'www.facebook.com' not 'https://www.facebook.com/'.If the web")
        print("address is given in correct way than try to restart you computer")
        print("\n\n\n")
        print("MADE BY @FATIN SHADAB".center(COLS))
        print("\n\n\n")
        input("\nEnter to go to 'HOME' ...")
        
    if (msg):
        print()
        print(f"🔔 {msg}\n".center(COLS))

    if not has_masterpass():
        msg = set_masterpass()
        return ui(win, msg)

# The MAIN FUNCTION TO RUN THE SYSTEM
def system() -> None:
    if OS_TYPE != 'nt':
        print(f"{'*'*(COLS//2)}".center(COLS))
        print(f"ONLY SUPPORTED OS : WINDOWS".center(COLS))
        print(f"{'*'*(COLS//2)}".center(COLS))
        input()
        return

    response = unblock("www.test.com")

    if response == PERMISSION_ERROR:
        print(f"{'*'*(COLS//2)}".center(COLS))
        print(f"RUN THE FILE WITH ADMINISTRATION ACCESS!".center(COLS))
        print(f"{'*'*(COLS//2)}".center(COLS))
        input()
        return

    if response == FILE_NOT_FOUND_ERROR:
        print(f"{'*'*(COLS//2)}".center(COLS))
        print(f"WINDOWS 'hosts' file not found in : {HOST_FILE}".center(COLS))
        print(f"{'*'*(COLS//2)}".center(COLS))
        input()
        return

    winName  : str = WINDOWS[0]
    msg      : str = None

    while True:
        if winName != WINDOWS[0]:
            ui(winName, msg)

        if winName == WINDOWS[1]:
            website : str = input("Enter the webaddress : ").strip()
            
            if len(website) >= 3:
                response = block(website)

                if response == 1:
                    msg = f"{website} added to the blocklist."
                if response == 0:
                    msg = f"{website} alrady exists in blocklist"
            else:
                    msg = f"Invalid {website}!"
            
            winName = WINDOWS[0]
        
        if winName == WINDOWS[2]:
            if not valid_masterpass():
                msg = f"Invalid MASTERPASS !"
            else:
                ui(winName, msg)
                website : str = input("Enter the webaddress : ")
                response = unblock(website)

                if response == 1:
                    msg = f"{website} removed from the blocklist."
                if response == 0:
                    msg = f"{website} didn't found in blocklist"
            
            winName = WINDOWS[0]

        if winName == WINDOWS[3]:
            if not valid_masterpass():
                msg = f"Invalid MASTERPASS !"
            else:
                ui(winName, msg)
                show_list()
                input(f"\nEnter TO GO TO '{WINDOWS[0]}' ...")
            
            winName = WINDOWS[0]
        
        if winName == WINDOWS[4] or winName == WINDOWS[5]:
            winName = WINDOWS[0]

        if winName == WINDOWS[6]:
            os.system("cls")
            exit(0)

        #print(f"here {winName}")
        ui(winName, msg)
        msg = None
        option : str = input("Select a option [1/2/3/4/5/6] : ")

        try:
            winName = WINDOWS[int(option)]
        except (IndexError, ValueError) as e:
            msg = f"Invalid Option {option}!"

    return


if __name__ == "__main__":
    try:
        system()
    except KeyboardInterrupt:
        pass