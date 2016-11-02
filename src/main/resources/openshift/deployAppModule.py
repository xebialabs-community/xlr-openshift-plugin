#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import subprocess

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
cmdProject ="%s project %s" % (ocCmd, ocProject)
cmdDeploy = "%s new-app %s:%s --name=%s " % (ocCmd, dockerImage, dockerTag, appName)
cmdExpose = "%s expose service %s" % (ocCmd, appName)
script = """

%s && %s && %s && %s && %s status

""" % (cmdLogon, cmdProject, cmdDeploy, cmdExpose, ocCmd)

print script
print "-------------------------"

proc = subprocess.Popen( script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# set variables
output = proc.stdout.read()
error = proc.stderr.read()

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
