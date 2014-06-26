"""
    Parse database details from Moodle config file and open specified DB app.
    No error handling. Ignores anything other than PostgreSQL and MySQL.
    tonyblundell@gmail.com
"""

import os
import re
import subprocess

def main():
    path = os.path.join(os.getcwd(), 'config.php')
    connection_info = get_connection_info(path)
    launch_database(connection_info)

def get_connection_info(path):
    connection_info = {}
    with open(path) as open_file:
        for line in open_file.readlines():
            for setting in ('dbtype', 'dbname', 'dbuser', 'dbpass'):
                pattern = '{setting}.*\'(.+)\''.format(setting=setting)
                matches = re.search(pattern, line)
                if matches:
                    connection_info[setting] = matches.groups()[0]
    return connection_info

def launch_database(connection_info):
    if connection_info['dbtype'] == 'pgsql':
        cmd = 'psql {dbname}'
    elif connection_info['dbtype'].startswith('mysql'):
        cmd = 'mysql --user={dbuser} --password={dbpass} {dbname}'
    cmd = cmd.format(**connection_info)
    subprocess.call(cmd.split())

if __name__=='__main__':
    main()
