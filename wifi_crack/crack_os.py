import os


def commandExists(command):
    def canExecute(file):
        return os.path.isfile(file) and os.access(file, os.X_OK)

    for path in os.environ["PATH"].split(os.pathsep):
        file = os.path.join(path, command)
        if canExecute(file):
            return True
    return False

def crack():
    print("Checking for root access...")
    user = os.popen("whoami").read()
    if 'root' not in user:
        print('You need to be the root user to run this program and you are running as ' + user + '  Try sudo python <ScriptName>.py')
        print('Exiting...')
        quit()
    else:
        print('Good job, you\'re root.')


    print("Trying to activate the default wlp2s0 network...")
    if not commandExists("ifconfig"):
        print("You will need the command 'ifconfig' to continue.")
        quit()
    status = os.popen("ifconfig wlp2s0 up").read()
    if 'No such device' in status:
        print("It seems your wireless device is not named wlp2s0, so you're going to need to enter it manually.")
        winame = eval(input('Wireless Device Name: '))
    else:
        winame = "wlp2s0"
    print("Wireless device enabled!")

    print("Checking for available wireless networks...")

    stream = os.popen("iwlist " + winame + " scan")
    print("Available Networks:")

    networksfound = 0
    for line in stream:
        if "ESSID" in line:
            networksfound += 1
            print(" " + line.split('ESSID:"', 1)[1].split('"', 1)[0])

    if networksfound == 0:
        print("Looks like we didn't find any networks in your area. Exiting...")

        quit()
    network = str(input("Please enter your network: "))
    tpass =input("Please enter the network's pass (Blank for none): ")
    if tpass == '':
        os.popen("iwconfig " + winame + " essid " + network)
    else:
        connectstatus = os.popen("iwconfig " + winame + " essid " + network + " key s:" + tpass)
    print("Connecting...")

    if not commandExists("dhclient"):
        print("Looks like there isn't a dhclient program on this computer. Trying dhcpd (Used with Arch)")

        con2 = os.popen("dhcpcd " + winame).read()
        print()
        con2
        if not commandExists("dhcpcd"):

            quit()
    else:
        os.popen("dhclient " + winame)
    ontest = os.popen("ping -c 1 google.com").read()
    if ontest == '':
        print("Connection failed. (Bad pass?)")

        quit()
    print("Connected successfully!=========== "+ str(tpass))




crack()

