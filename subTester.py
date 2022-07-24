import requests
from tqdm import tqdm
import sys
from sys import argv
from pyfiglet import Figlet
from boxing import boxing
import argparse
import datetime

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(usage="python3 subTester.py [OPTIONS]", description="Test subdomains")
    parser.add_argument("-d", "--domain", type=str, metavar="", required=True, help="Domain of the target")
    parser.add_argument("-w", "--wordlist", type=str, metavar="", required=True, help="Wordlist that will be used")
    parser.add_argument("-sF", "--saveFile", type=str, metavar="", help="Save the output to a file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--automatically", action="store_true", help="Automatically shows successful domains without progress bar")
    group.add_argument("-v", "--verbose", action="store_true", help="Shows all tested subdomains")

    if len(argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    # Create the box
    font = Figlet(font='big')
    rendfont = font.renderText("subTester")
    box = boxing(f"{rendfont} Coded by: Lorenzo", style="classic")
    print(box)

    # Does the request
    lines = []
    subDomains = []
    with open(args.wordlist, "r") as sub:
        lines = sub.readlines()
        print(f"[*]Testing subdomains | Test started at {datetime.datetime.now()}\n")

        if args.automatically:
            print("[+]Subdomains availables:")
            for i in lines:
                try:
                    pageUrl = f"https://{i.strip()}.{args.domain}/"
                    pageContent = requests.get(pageUrl, timeout=0.5)
                    if pageContent.status_code == 200:
                        print(f"\n     https://{i.strip()}.{args.domain}/")
                        if args.saveFile:
                            subDomains.append(f"https://{i.strip()}.{args.domain}/")
                except requests.exceptions.ConnectionError:
                    pass
            sub.close()

        elif args.verbose:
            print("[+]Verbose")
            for i in lines:
                try:
                    pageUrl = f"https://{i.strip()}.{args.domain}/"
                    pageContent = requests.get(pageUrl, timeout=0.5)
                    print(f"\n     https://{i.strip()}.{args.domain}/ | Available")
                except requests.exceptions.ConnectionError:
                    print(f"\n     https://{i.strip()}.{args.domain}/")
                if args.saveFile:
                    subDomains.append(f"https://{i.strip()}.{args.domain}/")
            sub.close()

        else:
            for i in tqdm(lines, position=0, leave=True, desc="Progress"):
                try:
                    pageUrl = f"https://{i.strip()}.{args.domain}/"
                    pageContent = requests.get(pageUrl, timeout=0.5)
                    if pageContent.status_code == 200:
                        subDomains.append(f"https://{i.strip()}.{args.domain}/")
                except requests.exceptions.ConnectionError:
                    pass
            sub.close()
            print("\n[+]Subdomains availables:")
            for i in subDomains:
                print(f"\n     {i}")

    if args.saveFile:
        with open(args.saveFile, "w") as fl:
            for i in subDomains:
                fl.write(i)
                fl.write("\n")
            fl.close()

# Checks if it's the main program
if __name__ == "__main__":
    main()
else:
    print("Cannot be imported")