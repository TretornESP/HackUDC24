import os
import sys
import subprocess

def clone_repository(url):
    # Split repository and branch from the URL
    parts = url.split('/')
    repository = parts[-2]
    branch = parts[-1]

    # Clone the repository
    clone_url = f'https://github.com/TretornESP/{repository}'
    subprocess.run(['git', 'clone', clone_url])
    
    # Change directory to the cloned repository
    os.chdir(repository)

    # chmod +x master/*.sh && chmod +x worker/*.sh
    subprocess.run(['chmod', '+x', 'master/*.sh'])
    subprocess.run(['chmod', '+x', 'worker/*.sh'])

    # mkdir -p certs
    subprocess.run(['mkdir', '-p', 'certs'])

    # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/tretornesp.key -out certs/tretornesp.crt
    subprocess.run(['openssl', 'req', '-x509', '-nodes', '-days', '365', '-newkey', 'rsa:2048', '-keyout', 'certs/tretornesp.key', '-out', 'certs/tretornesp.crt'])

    # Edit docker-compose.yml file
    with open('docker-compose.yml', 'r') as file:
        content = file.read()

    content = content.replace('{{ repository }}', repository)
    content = content.replace('{{ branch }}', branch)

    with open('docker-compose.yml', 'w') as file:
        file.write(content)

def main():
    # Check if the URL is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <github_url>")
        sys.exit(1)

    github_url = sys.argv[1]

    # Clone repository, edit docker-compose.yml, and run docker-compose up --build
    clone_repository(github_url)

    print("Now edit docker-compose.yml and master.cfg to set keys and addresses")

    # Not composing because further configuration is needed
    # subprocess.run(['docker-compose', 'up', '--build'])

if __name__ == "__main__":
    main()