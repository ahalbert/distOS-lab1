import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:8080')
print s.add(2)  # Returns 5

# Print list of available methods
# print s.system.listMethods()
