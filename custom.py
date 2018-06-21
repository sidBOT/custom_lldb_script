##########################

####CREDITS:SidBOT####

##########################

#USAGE
#see usage function or type usage in lldb





#coding:utf-8
import lldb
import commands
import re
import optparse
import shlex
import platform
import struct

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
        print >>result, hilite('Please input the address!', 0, 1)
        return
    addresses = command.split(' ')
    get_aslr = get_ASLR()
    if get_aslr:
        
        if addresses[0] == "-f": #only use if you want to bp directly to an IDA offset
            addr = format(eval("%s+%s" % (addresses[1], get_aslr)), '#04x')
            debugger.HandleCommand('br set -a "%s"' % (addr))
        
        else:
            debugger.HandleCommand('br set -a "%s+%s"' % (get_aslr, command))

    else:
        print >>result, hilite('ASLR not found! (Did you attach a process yet?)', 0, 1)

def getASLR(debugger, command, result, internal_dict):

    get_aslr = get_ASLR()
    if get_aslr:
        
        print >>result, 'ASLR Slide: ' + hilite(get_aslr, 1, 0)
    else:
        print >>result, hilite('ASLR not found! (Did you attach a process yet?)', 0, 1)

def credits(debugger, command, result, internal_dict):

    print >>result, '@M4skM4n007'

def write(debugger, command, result, internal_dict):
    
    
    if not command:
        print >>result, hilite('Please input the addresses!', 0, 1)
        return

    addresses = command.split(' ')
    get_aslr = get_ASLR()

    if get_aslr:

        if addresses[0] != '-f':
            debugger.HandleCommand('memory write -s 4 %s %s' % (addresses[0], addresses[1]))
            #print >>result, 'memory write -s 4 "%s" "%s"' % (addresses[0], addresses[1])
            
        elif addresses[0] == '-f':
            addr = format(eval("%s+%s" % (addresses[1], get_aslr)), '#04x')
            debugger.HandleCommand('memory write -s 4 %s %s' % (addr, addresses[2]))

        else:
            print >>result, hilite('Please enter 2 values (Address and your hex value)', 0, 1)

    else:
        print >>result, hilite('ASLR not found! (Did you attach a process yet?)', 0, 1)

def get_adr(debugger, command, result, internal_dict):
    
    if not command:
        print >>result, hilite('Please input the address!', 0, 1)
        return
    get_aslr = get_ASLR()
    if get_aslr:
        print >>result, hilite(format(eval("%s-%s" % (command, get_aslr)), '#04x'), 1, 0)
    else:
        print >>result, hilite('ASLR not found! (Did you attach a process yet?)', 0 , 1)


def hilite(string, status, bold):
    attr = []
    if status:
        # blue
        attr.append('34')
    else:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


def convert_to(debugger, command, result, internal_dict):
    
    if not command:
        print >>result, hilite('Please input the address!', 0, 1)
        return

    addresses = command.split(' ')

    if addresses[0] == '-f' or addresses[0] == '-float':
        splt = addresses[1].split('0x')
        new_add = splt[1]
        res = struct.unpack('!f', new_add.decode('hex'))[0]
        s = str(res)
        print >>result, 'Float Value: ' + hilite(s, 1, 0)

    elif addresses[0] == '-h' or addresses[0] == '-hex':
        res = hex(struct.unpack('<I', struct.pack('<f',float(addresses[1])))[0])
        print >>result, 'Hex Value: ' + hilite(res, 1, 0)

    else:
        print >>result, hilite('invalid input', 0, 1)


def list_address(debugger, command, result, internal_dict):
    
    if not command:
        print >>result, hilite('Please input the address!', 0, 1)
        return

    get_aslr = get_ASLR()
    addresses = command.split(' ')

    if get_aslr and len(addresses) == 3:
        if addresses[0] == '-a' or addresses[0] == '-add':
            list_of_addresses[addresses[1]] = addresses[2]
            print >>result, hilite(addresses[2] + ' has been added', 1, 0)
    elif addresses[0] == '-s' or addresses[0] == '-show':
        if not list_of_addresses:
            print >>result, 'Empty'
            return
        for key, value in list_of_addresses.iteritems():
            print >>result, 'Address: ' + hilite(key,1,0) + ' Value: ' + hilite(value, 1, 0)

        else:
            return
    elif addresses[0] == '-r' or addresses[0] == '-remove':
        print >>result, hilite('Address removed', 1, 0)
        del list_of_addresses[addresses[1]]
    else:
        print >>result, hilite('ASLR not found! (Did you attach a process yet?) or invalid command', 0, 1)

def usage(debugger, command, result, internal_dict):
    
    
    print >> result, 'set breakpoint with ASLR added: ' + hilite('set-bp 0xADDRESS',1,1)
    print >> result, 'set breakpoint without ASLR added: ' + hilite('set-bp -f 0xADDRESS',1,1)
    print >> result, 'write 4 bytes to memory: ' + hilite('write 0xADDRESS 0xVALUE',1,1)
    print >> result, 'write 4 bytes directly to IDA Offset: ' + hilite('write -f 0xADDRESS 0xVALUE',1,1)
    print >> result, 'get IDA offset (ASLR removed) ' + hilite('get-adr 0xADDRESS',1,1)
    print >> result, 'get ASLR Slide: ' + hilite('ASLR',1,1)
    print >> result, 'Convert hex to float: ' + hilite('convert -f 0xVALUE',1,1)
    print >> result, 'Convert float to hex: ' + hilite('convert -h 0xVALUE',1,1)
    print >> result, 'Save an address and function name for future reference: ' + hilite('list-add -a 0xADDRESS nameOfTheFunction',1,1)
    print >> result, 'list down all the saved addresses with their names: ' + hilite('list-add -s',1,1)
    print >> result, 'delete address from the saved list ' + hilite('list-add -r 0xADDRESS',1,1)





def __lldb_init_module(debugger, internal_dict):
    
    #debugger.HandleCommand('command script import custom.py')
    global list_of_addresses
    list_of_addresses = {}
    debugger.HandleCommand('command script add -f custom.aslr set-bp')
    debugger.HandleCommand('command script add -f custom.write write')
    debugger.HandleCommand('command script add -f custom.credits credit')
    debugger.HandleCommand('command script add -f custom.getASLR ASLR')
    debugger.HandleCommand('command script add -f custom.get_adr get-adr')
    debugger.HandleCommand('command script add -f custom.convert_to convert')
    debugger.HandleCommand('command script add -f custom.list_address list-add')
    debugger.HandleCommand('command script add -f custom.usage usage')
    
    print hilite('Custom script successfully injected. Author - ', 1, 0) + hilite('@M4skM4n007', 1, 1)
    print hilite('type "usage" for help', 1, 0)









