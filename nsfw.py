"Used for updating the nsfw emotes list"
import os
import requests
import json

URL = 'https://api.github.com/repos/Rothera/bpm/contents/tags'


def fetch_nsfw_emotes(do_print=True):
    print("Searching for NSFW emotes...")
    nsfw = []
    data_file = requests.get(URL).text
    data = json.loads(data_file)
    for e in data:
        print('...  in ' + e['name'])
        url = e['download_url']
        tag = requests.get(url).text
        jtag = json.loads(tag)
        for emote, val in jtag.items():
            if '+nsfw' in val:
                nsfw.append(emote[1:])

    with open('nsfw.txt', 'w') as file:
        file.writelines("\n".join(nsfw))

    if do_print:
        print(str(get_nsfw_emotes()))


def get_nsfw_emotes():
    if not os.path.isfile('nsfw.txt'):
        print('Fetching nsfw emotes')
        fetch_nsfw_emotes(False)

    with open('nsfw.txt', 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    fetch_nsfw_emotes()
