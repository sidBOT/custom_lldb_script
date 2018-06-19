##########################

####CREDITS:SidBOT####

##########################

#USAGE
#set-bp 0xADDRESS : set breakpoint at the address with aslr added
#ASLR : Gives you the aslr slide
#write 0xADDRESS 0xVALUE : write to memory. Similar as => memory write -s 4 0xADDRESS 0xVALUE
    #eg: write 0x1001E0780 0xD65F03C0
#get-adr 0xADDRESS : get the address - aslr. To find IDA Offsets
#Follow me on twitter: @M4skM4n007





#coding:utf-8
import lldb
import commands
import re
import optparse
import shlex

def get_ASLR():
    
    interpreter = lldb.debugger.GetCommandInterpreter()
    returnObject = lldb.SBCommandReturnObject()
    interpreter.HandleCommand('image list -o', returnObject)
    output = returnObject.GetOutput();
    match = re.findall(r'.+(0x[0-9a-fA-F]+)', output)
    #print output
    if match:
        
        return match[1]
    else:
        return None

def aslr(debugger, command, result, internal_dict):
    
    
    
    if not command:
        print >>result, 'Please input the address!'
        return
    addresses = command.split(' ')
    get_aslr = get_ASLR()
    if get_aslr:
        
        debugger.HandleCommand('br set -a "%s+%s"' % (get_aslr, command))
    
    elif addresses[0] == "-f": #Force breakpoint with -f (under development)
        debugger.HandleCommand('br set -a "%s"' % (addresses[1]))

    else:
        print >>result, 'ASLR not found! (Did you attach a process yet?)'

def getASLR(debugger, command, result, internal_dict):

    get_aslr = get_ASLR()
    if get_aslr:
        
        print >>result, 'ASLR Slide: ' + get_aslr
    else:
        print >>result, 'ASLR not found! (Did you attach a process yet?)'

def credits(debugger, command, result, internal_dict):

    print >>result, '@M4skM4n007'

def write(debugger, command, result, internal_dict):
    
    
    if not command:
        print >>result, 'Please input the addresses!'
        return

    addresses = command.split(' ')
    get_aslr = get_ASLR()

    if get_aslr:

        if len(addresses) == 2:
            debugger.HandleCommand('memory write -s 4 %s %s' % (addresses[0], addresses[1]))
            #print >>result, 'memory write -s 4 "%s" "%s"' % (addresses[0], addresses[1])

        else:
            print >>result, 'Please enter 2 values (Address and your hex value)'

    else:
        print >>result, 'ASLR not found! (Did you attach a process yet?)'

def get_adr(debugger, command, result, internal_dict):
    
    if not command:
        print >>result, 'Please input the address!'
        return
    get_aslr = get_ASLR()
    if get_aslr:
        print >>result, format(eval("%s-%s" % (command, get_aslr)), '#04x')
    else:
        print >>result, 'ASLR not found! (Did you attach a process yet?)'


def __lldb_init_module(debugger, internal_dict):
    
    #debugger.HandleCommand('command script import custom.py')
    debugger.HandleCommand('command script add -f custom.aslr set-bp')
    debugger.HandleCommand('command script add -f custom.write write')
    debugger.HandleCommand('command script add -f custom.credits credit')
    debugger.HandleCommand('command script add -f custom.getASLR ASLR')
    debugger.HandleCommand('command script add -f custom.get_adr get-adr')
    
    print 'Custom script by @M4skM4n007'









