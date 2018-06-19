## custom_lldb_script

# INSTALLATION

Make a file .lldbinit in your home directory (.lldbinit is the first thing that lldb reads when it loads) do cd ~ to go to your home directory
	
	if you run as root, then home dir = /var/root
	if you run withoutroot, home dir = /var/mobile
	
	
Add the following to the file (.lldbinit) 

	settings set target.load-cwd-lldbinit true
	command script import custom.py
	
	
Place custom.py in /var/mobile (working directory)
start lldb

Commands:
	
	ASLR : get aslr slide
	set-bp 0xaddress : set breakpoint (ASLR added)
	write 0xaddress 0xvalue : write to memory, same as => memory write -s 4 0xaddress 0xvalue (address frorm lldb)
	get-adr 0xaddress : [get address - aslr], to find the IDA Address


<img src='https://media.giphy.com/media/uBn76OHK83u6tuIiMM/giphy.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />
