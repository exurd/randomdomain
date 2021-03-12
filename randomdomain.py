import requests
import random
import webbrowser
import argparse
import time
from time import sleep
import unidecode

parser = argparse.ArgumentParser(description="Finds domains by using random words in a text file", epilog="This program has the WTFPL license. DO WHAT THE F*CK YOU WANT TO.")
parser.add_argument('--text_file', '-t', type=str,  help="The text file that will be used to grab the words.", default="en_words_edited.txt")
parser.add_argument('--domain_extension', '-ext', type=str,  help="What the domain extension will end with. Default is random extension.", default="random")
parser.add_argument('--save_links', '-sl', help="Saves working domains to the Wayback Machine automatically. It will open the internet browser. (Note: it will not save outlinks.)", action='store_true')
parser.add_argument('--save_new_links', '-snl', help="Only saves the links if it has not been archived by the Wayback Machine. Will supersede --save_links. [DOES NOT WORK YET.]", action='store_true')
parser.add_argument('--repeat', '-r', help="Keeps repeating without quitting the program.", action='store_true')
parser.add_argument('--double', '-d', help="Uses two random words instead of one. May be impossible to find a domain.", action='store_true')
parser.add_argument('--no_prompt', '-a', help="No prompt will appear to open the link.", action='store_true')
parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
args, unknown = parser.parse_known_args()

def yes_or_no(question): # for y/n styled questions to work
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

 # read and split words
lines = open(args.text_file, encoding="utf8").read().splitlines()

if args.domain_extension == "random":
    exts = open('extensions.txt', encoding="utf8").read().splitlines()


# main code
while True:
    randomword = random.choice(lines) # pick random word
    
    if args.domain_extension == "random": # check if they wanted a random domain extension
        ext = random.choice(exts) # pick random ext
    else:
        ext = args.domain_extension # use ext they wanted
    
    if args.double == True: # ask if they wanted to choose two words
        randomword2 = random.choice(lines) # pick another random word
        # next we will merge the whole thing together
        domainname = "https://www." + unidecode.unidecode(randomword) + unidecode.unidecode(randomword2) + ext
    else:
        domainname = "https://www." + unidecode.unidecode(randomword) + ext
    print("Trying " + domainname + " ...")
    try: # we will now try to connect to the domain
        request = requests.get(domainname) # send request; if it fails then we try another domain
        print('Web site exists; try going to: ' + domainname + " (Caution: It might be a domain on sale.)") # it works; say something about it
        
        if args.save_new_links == True:
            print("WARNING! Checking for new links doesn't work yet!") # warn user that the new link checker doesnt work yet
            wayresponse = requests.get("http://archive.org/wayback/available?url=" + domainname)
            wayresponse.json()
            if wayresponse == '{"archived_snapshots":{}}':
                print("Found new link not archived by the Wayback Machine! Saving via the Wayback Machine...")
                print("Giving 45 seconds to wait for the process to finish...")
                webbrowser.open("https://web.archive.org/save/" + domainname)
                time.sleep(45)
            else:
                print("Exists in the Wayback Machine (Status 200). Skipping...")

        if args.save_links == True and args.save_new_links == False: # saves the link to the wayback machine
            print("Saving via the Wayback Machine...")
            print("Giving 45 seconds to wait for the process to finish...")
            webbrowser.open("https://web.archive.org/save/" + domainname)
            time.sleep(45)
        
        if args.no_prompt == False:
            if yes_or_no("Do you want to go to this link?") == True: # asks to open the link
                webbrowser.open(domainname)
        
        if args.repeat == True: # if enabled it will try to find another working domain
            print("Okay. Finding another domain...")
        else:
            print("Exiting the program...")
            exit()
    except requests.ConnectionError:
        print('Domain does not exist or cannot connect to domain. Trying another domain...') #it failed; it will now try another domain