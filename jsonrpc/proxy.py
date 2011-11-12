import urllib2, random
from jsonrpc._json import loads, dumps
from jsonrpc.types import *

class ServiceProxy(object):
  def __init__(self, service_url, service_name=None, version='1.0'):
    self.__version = str(version)
    self.__service_url = service_url
    self.__service_name = service_name

  def __getattr__(self, name):
    if self.__service_name != None:
      name = "%s.%s" % (self.__service_name, name)
    return ServiceProxy(self.__service_url, name, self.__version)
  
  def __repr__(self):
    return {"jsonrpc": self.__version,
            "method": self.__service_name}
  
  def __call__(self, *args, **kwargs):    
    if len(kwargs):
       params = kwargs
    else:
       params = args
    
    #if Any.kind(params) == Object and self.__version != '2.0':
    #  raise Exception('Unsupport arg type for JSON-RPC 1.0 '
    #                 '(the default version for this client, '
    #                'pass version="2.0" to use keyword arguments)')
    # req = urllib2.Request(self.__service_url, )
    r = urllib2.urlopen(self.__service_url,
                        dumps({
                          "jsonrpc": self.__version,
                          "method": self.__service_name,
                          'params': params,
                          'id': str(random.randint(10000, 100000000))}),
                        15).read()
    y = loads(r)
    if u'error' in y:
        pass
    return y
