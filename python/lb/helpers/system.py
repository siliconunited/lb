# system.py
# Contains helper functions related to the system


# Handles putting an actual name to the sys.platform value
def get_sys_name(val):
    return {
        'linux2':'Linux',
        'win32':'Windows',
        'cygwin':'Windows/Cygwin',
        'darwin':'MacOSX',
        'os2':'OS/2',
        'os2emx':'OS/2 EMX',
        'riscos':'RiscOS',
        'atheos':'AtheOS'
    }.get(val, 'Other') # Other is default if nothing else is found
