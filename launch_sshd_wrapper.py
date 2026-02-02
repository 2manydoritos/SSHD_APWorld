"""
Launcher wrapper for SSHD Archipelago Client
"""
import zipfile
import sys

# Add .apworld to path
APWORLD_PATH = r'C:\ProgramData\Archipelago\custom_worlds\sshd.apworld'
sys.path.insert(0, APWORLD_PATH)

# Extract and execute SSHDClient
zf = zipfile.ZipFile(APWORLD_PATH)
code = zf.read('sshd/SSHDClient.py').decode('utf-8')

# Execute with proper context
exec(code, {
    '__name__': '__main__',
    '__file__': f'{APWORLD_PATH}/sshd/SSHDClient.py',
    '__package__': 'sshd'
})
