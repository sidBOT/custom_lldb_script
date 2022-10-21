## custom_lldb_script

# INSTALLATION

Make a file ```.lldbinit``` in your home directory (.lldbinit is the first thing that lldb reads when it loads) do ```cd ~``` to go to your home directory
	
	FOR IPHONE
	if you run as root, then home dir = /var/root
	if you run withoutroot, home dir = /var/mobile
	
	FOR MAC
	```cd ~```
	
	
Add the following to the file (.lldbinit) 

	settings set target.load-cwd-lldbinit true
	command script import custom.py
	
	
Place custom.py in /var/mobile (working directory)
start lldb

# Usage
Commands:
	
	ASLR : get aslr slide
	set-bp 0xaddress : set breakpoint (ASLR added)
	set-bp -f 0xaddress : force set breakpoint
	write 0xaddress 0xvalue : write to memory, same as => memory write -s 4 0xaddress 0xvalue (address frorm lldb)
	write -f 0xaddress 0xvalue : write to memory at the IDA offset directly
	get-adr 0xaddress : [get address - aslr], to find the IDA Address
	convert -f 0xvalue : convert hex to 32 bit single precision float value
	convert -h floatValue : convert float value to hexadecimal
	list-add -a 0xaddress functionName : save address and the name for it in a list for future reference 
	list-add -s : show all the saved addresses in the list
	list-add -r 0xaddress : remove the address from the list
	usage : type this in lldb for help


## Video Walkthrough

Demo Video

<img src='https://media.giphy.com/media/OO2FmCV9okkbBotVqj/giphy.gif' title='Test' width='' alt='Video Walkthrough' />
