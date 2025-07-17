#!/bin/bash
tools=(
    nmap
    nikto
    sqlmap
    waybackurls
    nuclei
    dirsearch
)

for tool in "${tools[@]}"; do
    if ! command -v $tool &> /dev/null; then
        echo "Installing $tool..."
        case $tool in
            dirsearch)
                git clone https://github.com/maurosoria/dirsearch.git
                ;;
            waybackurls)
                go install github.com/tomnomnom/waybackurls@latest
                ;;
            nuclei)
                go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
                ;;
            *)
                sudo apt install $tool -y
                ;;
        esac
    fi
done
