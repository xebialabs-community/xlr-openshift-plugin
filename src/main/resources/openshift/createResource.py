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

stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()

try:
    connection = LocalConnection.getLocalConnection()
    targetYaml = connection.getTempFile('resource', '.yaml')
    OverthereUtils.write( String(resourceYaml).getBytes(), targetYaml)
    cmdLogon  = "%s login --server=%s -u %s -p %s --insecure-skip-tls-verify" % (ocCmd, ocUrl, ocUsername, ocPassword)
    cmdProject ="%s project %s" % (ocCmd, ocProject)
    cmdCreate = "%s create -f %s -n %s " % (ocCmd, targetYaml.getPath(), ocProject)
    script = """
    %s
    %s
    %s
    """ % (cmdLogon, cmdProject, cmdCreate)

    #print script
    print "-------------------------"

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
    print "----"
    print "#### Output:"
    print output
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
