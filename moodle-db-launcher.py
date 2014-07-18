"""
    Parse database details from Moodle config file and open specified DB app.
    No error handling. Ignores anything other than PostgreSQL and MySQL.
    tonyblundell@gmail.com
"""

import os
import re
import subprocess

def main():
    path = get_config_file_path(os.getcwd())
    connection_info = get_connection_info(path)
    launch_database(connection_info)

def get_config_file_path(path):
    file_path = os.path.join(path, 'config.php')
    if os.path.isfile(file_path):
        return file_path
    path = os.path.sep.join(path.split(os.path.sep)[:-1])
    if path:
        return get_config_file_path(path)
    raise Exception('Config file not found')

def get_connection_info(path):
    settings = ('dbtype', 'dbname', 'dbuser', 'dbpass')
    connection_info = {}
    with open(path) as open_file:
        for line in open_file.readlines():
            for setting in settings:
                pattern = '{setting}.*[\'\"](.+)[\'\"]'.format(setting=setting)
                matches = re.search(pattern, line)
                if matches:
                    connection_info[setting] = matches.groups()[0]
    diff = set(settings) - set(connection_info.keys())
    if not diff:
        return connection_info
    missing = ', '.join(diff) 
    raise Exception('Settings not found in config file: {}'.format(missing))

def launch_database(connection_info):
    if connection_info['dbtype'] == 'pgsql':
        cmd = 'psql {dbname}'
    elif connection_info['dbtype'].startswith('mysql'):
        cmd = 'mysql --user={dbuser} --password={dbpass} {dbname}'
    cmd = cmd.format(**connection_info)
    subprocess.call(cmd.split())

if __name__=='__main__':
    main()
