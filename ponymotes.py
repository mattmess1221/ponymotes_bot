import re
import emotes
import nsfw


"This pattern finds emotes"
EMOTE_PATTERN = re.compile(  # [Some text](/ponies-flags "alt")
    r'\[([^[\]]*?)\]\(\/(?![ur]\/)([^\s()[\]-]+?)((?:-[\w\d]+)*) *(?: \"(.*)\" *)?\)')  # noqa (line's too long)

NSFW_EMOTES = nsfw.get_nsfw_emotes()
print('Found %d nsfw emotes' % len(NSFW_EMOTES))

TEXT = 1
EMOTE = 2
MODIFIERS = 3
TOOLTIP = 4


class Ponymote:

    def __init__(self, pony):
        self.text = pony.group(TEXT)
        self.name = pony.group(EMOTE)
        mods = pony.group(MODIFIERS)
        self.flags = mods.split('-')[0:] if mods else []
        self.tooltip = pony.group(TOOLTIP)
        self.nsfw = self.name in NSFW_EMOTES

    def is_default(self):
        return emotes.getEmote(self.name)

    def view_url(self):
        return "http://ponymotes.net/view/" + self.name + "-".join(self.flags)

    def __str__(self):
        return self.name


def parse(post):
    """Finds emotes in a post

    Returns a list of Ponymote"""
    matches = EMOTE_PATTERN.finditer(post)
    motes = []
    for ponymote in matches:
        motes.append(Ponymote(ponymote))
    return motes
