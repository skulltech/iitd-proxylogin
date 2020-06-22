# iitd-proxylogin
Dependency free Python script for logging in to IIT Delhi proxy service.

_iitd-proxylogin_ is heavily inspired from [this script](https://github.com/abhishek4747/Proxy-login)—which is 5 years old, and the author has been inactive for a long time, so I created a fresh repo instead of sending a pull request. Changes I made are the following 
- Ported the code to Python 3.
- Added support for config file and interactive mode so that the password does not get leaked to the shell history.
- Added support for different CLI switches for increased usability.


## Usage

```console
sumit@HAL9000:~/Sysadmin/iitd-proxylogin$ python3 proxylogin.py 
usage: proxylogin.py [-h] (-c CONFIG | -i) [-r] [-s] [-p]

dependency free Python script for logging in to IIT Delhi proxy service
created by Sumit Ghosh @SkullTech

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration INI file containing credentials
  -i, --interactive     Interactive mode
  -r, --refresh         After logging in, keep running and refreshing
  -s, --skip-tls-verify
                        Foolishly accept TLS certificates signed by unkown
                        certificate authorities
  -p, --print-envvars   Print proxy configuration environment variables

available proxy categories are ['btech', 'dual', 'diit', 'faculty',
'integrated', 'mtech', 'phd', 'retfaculty', 'staff', 'irdstaff', 'mba',
'mdes', 'msc', 'msr', 'pgdip', 'visitor', 'student', 'guest']
```
