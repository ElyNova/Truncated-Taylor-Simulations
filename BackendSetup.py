import getpass, time
from qiskit import register, available_backends, get_backend

#set token
def signIn():
    try:
        import sys
        sys.path.append("../")
        import Qconfig
        qx_config = {
            "APItoken": Qconfig.APItoken,
            "url": Qconfig.config['url']
        }
        register(qx_config['APItoken'], qx_config['url'])
    except Exception as e:
        print(e)
        APIToken = getpass.getpass('\nPlease enter your token and press enter')
        qx_config = {
            "APItoken": APIToken,
            "url":'https://quantumexperience.ng.bluemix.net/api'
        }
        register(qx_config['APItoken'], qx_config['url'])
    print(available_backends())

def bestBackend():
    sim = int(input("\nAllow simulators [0/1]?"))
    list = available_backends({'local': False, 'simulator': sim})
    bestatus = [get_backend(backend).status for backend in list]
    best = min([x for x in bestatus if x['available'] is True], key = lambda x: x['pending_jobs'])
    print("Using backend: "+ best['name'])
    return best['name']
