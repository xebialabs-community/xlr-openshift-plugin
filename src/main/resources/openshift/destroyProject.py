#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys

from java.lang import Exception
from java.io import PrintWriter
from java.io import StringWriter

from com.xebialabs.overthere import CmdLine, ConnectionOptions, OperatingSystemFamily, Overthere
from com.xebialabs.overthere.local import LocalConnection
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils

ocUsername = openShiftServer['username']
ocPassword = openShiftServer['password']
ocUrl = openShiftServer['url']
ocHome = openShiftServer['ocHome']
ocCmd = "%soc" % (ocHome)


print "URL       = %s" % ocUrl
print "USERNAME  = %s" % ocUsername
print "OC        = %s" % ocCmd
print " "
cmdLogon  = "%s login --server=%s -u %s -p %s --insecure-skip-tls-verify" % (ocCmd, ocUrl, ocUsername, ocPassword)
cmdProject ="%s delete project %s" % (ocCmd, ocProject)
script = """

%s
%s

""" % (cmdLogon, cmdProject)
print script
print "-------------------------"

stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()

try:
    connection = LocalConnection.getLocalConnection()
    targetScript = connection.getTempFile('oc-script', '.bat')
    OverthereUtils.write( String(script).getBytes(), targetScript)
    targetScript.setExecutable(True)
    cmd = CmdLine.build( targetScript.getPath() )
    connection.execute( stdout, stderr, cmd )
except Exception, e:
    stacktrace = StringWriter()
    writer = PrintWriter( stacktrace, True )
    e.printStackTrace(writer)
    stderr.hadleLine(stacktrace.toString())

# set variables
output = stdout.getOutput()
error = stderr.getOutput()


if len(output) > 0:
    print "```"
    print output
    print "```"
else:
    print "----"
    print "#### Output:"
    print "```"
    print output
    print "```"

    print "----"
    print "#### Error stream:"
    print "```"
    print error
    print "```"
    print

    sys.exit(response.rc)
