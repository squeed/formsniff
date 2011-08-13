from twisted.internet import reactor
from twisted.web.server import Site

from twisted.web.resource import Resource
import sqlite3
import threading

from DataLogger import DataLogger

class HitPage(Resource):
    isLeaf = True
    def __init__(self):
        self.l = DataLogger.getInstance()


    def render_GET(self, request):
        lines = []
        hitid = None
        for row in self.l.get_all_hits():
            if row[0] != hitid:
                hitid = row[0]
                line = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % row[1:4]
            else:
                line = "<tr><td>&nbsp;</td><td>%s</td><td colspan=2>%s</td></tr>" % row[4:6]
            lines.append(line,)
    
        return str("<http><body><h2>Hits:</h2><table>%s</table></body></http>" % " ".join(lines))

def spawn(reactor, port):
    resource = HitPage()
    factory = Site(resource)
    reactor.listenTCP(port, factory)
