try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

class HTMLFirstLink(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.link = None
        self.target = None

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and not self.link:
            attr = dict(attrs)
            if 'href' in attr:
                self.link = attr['href']
                if 'target' in attr:
                    self.target = attr['target']
                else:
                    self.target = "_blank"