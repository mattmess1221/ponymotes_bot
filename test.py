import unittest
import ponymotes
import requests
import re


class TestEmoteReply(unittest.TestCase):

    def test_default(self):
        post = "[](/pinkiesad) I'm sad."
        emote = ponymotes.parse(post)[0]
        self.assertTrue(emote.is_default())

    def test_name(self):
        post = "[](/dieinahole)"
        emote = ponymotes.parse(post)[0]
        self.assertEqual('dieinahole', emote.name)

    def test_modifiers(self):
        post = "[](/cadence-intensifies-spin)"
        emote = ponymotes.parse(post)[0]
        self.assertIn(member="intensifies", container=emote.modifiers)

    def test_text(self):
        post = "[RIP Applejack](/gravestone)"
        emote = ponymotes.parse(post)[0]
        self.assertEqual('RIP Applejack', emote.text)

    def test_tooltip(self):
        post = '[](/fluttershy "Say what?")'
        emote = ponymotes.parse(post)[0]
        self.assertEqual('Say what?', emote.tooltip)

    def test_emotes_completion(self):
        import emotes
        try:
            css = requests.get('''\
https://raw.githubusercontent.com/Rothera/bpm/master/source-css/mylittlepony.css\
''').text
        except:
            return
        es = re.findall(r'a\[href\|="\/(.+?)"]', css)
        missing = []
        for e in es:
            if emotes.getEmote(e) is None and e not in missing:
                missing.append(e)
        self.assertTrue(len(missing) == 0, msg=' Missing emotes:%d \n\n%s '
                        % (len(missing), ', '.join(missing)))

    def test_colon(self):
        post = '[](/flutter:I)'
        emote = ponymotes.parse(post)[0]
        self.assertEqual('flutter:I', emote.name)

    def test_hashslash(self):
        post = '[](//#bneodestiny)'
        emote = ponymotes.parse(post)[0]
        self.assertEqual('/#bneodestiny', emote.name)

    def test_multiple_emotes(self):
        post = '[](/ppsad)[](/flutteryay)'
        emotes = ponymotes.parse(post)
        emotes = list(map(lambda v: v.name, emotes))
        self.assertListEqual(['ppsad', 'flutteryay'], emotes)

if __name__ == '__main__':
    unittest.main()
