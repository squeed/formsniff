from twisted.internet import reactor
#from twisted.web.server import Site
from twisted.web.resource import Resource

import javascript

class JavascriptResponse(Resource):
    """ Class that returns our malicious javascript"""
    
    isLeaf = True
    
    def render_GET(self, request):
        
        return javascript.pwn_js
