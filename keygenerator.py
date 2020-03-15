import subprocess

def get_key_pair(tunsafe_path):
    p1 = subprocess.Popen(args="TunSafe genkey", stdout=subprocess.PIPE, shell=True, cwd=tunsafe_path)
    private_key =  p1.communicate()[0].decode('utf-8')

    p2 = subprocess.Popen(args="TunSafe pubkey", stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True, cwd=tunsafe_path)
    p2.stdin.write(private_key.encode())
    public_key = p2.communicate()[0].decode('utf-8')

    return private_key, public_key


    