import socket
import common_ports
import re

def get_open_ports(target, port_range, verbose = False):
    open_ports = []
    try:
        ip = socket.gethostbyname(target)
        for port in range(port_range[0], port_range[1] + 1):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(0.5)

            if (s.connect_ex((ip,port)) == 0):
                open_ports.append(port)
            s.close()
            
    except socket.gaierror:
        if re.search('[a-zA-Z]',target):
            return 'Error: Invalid hostname'
        return 'Error: Invalid IP address'

    except:
        return 'Error: Invalid IP address'

    if verbose:
        url = None
        try:
            url = socket.gethostbyaddr(ip)[0]
        except:
            url = None

        verbose_output = 'Open ports for '
        
        if(url == None):
            verbose_output += '{ip}'.format(ip=ip)
        else:
            verbose_output +=  "{url} ({ip})".format(url=url,ip=ip)
        
        verbose_heading = '\nPORT     SERVICE\n'
        verbose_body=''
        for port in open_ports:
            verbose_body += '{port}'.format(port=port) + ' '*(9 - len(str(port))) + '{service_name}'.format(service_name=common_ports.ports_and_services[port])
            if(port != open_ports[len(open_ports)-1]):
                verbose_body += '\n'

        return verbose_output + verbose_heading + verbose_body
            
    return(open_ports)