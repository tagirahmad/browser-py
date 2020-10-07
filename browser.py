import errno
from collections import deque

import requests
from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore
import sys
import os

args = sys.argv

try:
    os.mkdir(args[1])
    # break
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
    pass


program_working = True
tabs_stack = deque()
while program_working:
    website_input = input()
    init(autoreset=True)

    if website_input.endswith('.com') or website_input.endswith('.org'):
        resp = requests.get('https://' + website_input)
        final_text = BeautifulSoup(resp.content, "html.parser")
        links_tags = [link for link in final_text.find_all('a')]
        links = [Fore.BLUE + str(link.get_text()) for link in final_text.find_all('a')]
        print(links_tags)
        for link in links_tags:
            for colored_link in links:
                final_text = str(final_text).replace(str(link), colored_link)
        final_text = BeautifulSoup(final_text, 'html.parser')
        print(final_text.get_text())
        file_name = website_input.split('.')[0].strip('https://')
        with open(f'{args[1]}/{file_name}.txt', 'w', encoding='UTF-8') as f1:
            f1.writelines(final_text.get_text())
            f1.close()
        tabs_stack.appendleft(file_name)

    if website_input == 'back':
        if len(tabs_stack) > 0:
            tabs_stack.popleft()
            with open(f'{args[1]}/{tabs_stack[-1]}.txt', 'r', encoding='UTF-8') as f_open:
                lines = f_open.readlines()
                for line in lines:
                    print(line)
    elif website_input == 'exit':
        program_working = False
