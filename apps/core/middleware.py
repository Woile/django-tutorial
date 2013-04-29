import logging


class Midexample(object):

    def process_request(self, request):
        
        logging.critical("[Middleware] Procesando Request. REQUEST: %s" % request.META['PATH_INFO'])
                    
        return None
    
    
    def process_response(self, request, response):
        
        logging.critical("[Middleware] Procesando Response. RESPONSE: %s" % response.content)
        
        return response