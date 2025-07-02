#!/bin/bash
bash $HOME/git/tumbleweed-setup/setup-scripts/01init
bash $HOME/git/tumbleweed-setup/setup-scripts/02patterns
bash $HOME/git/tumbleweed-setup/setup-scripts/03git
bash $HOME/git/tumbleweed-setup/setup-scripts/04syspkgs
bash $HOME/git/tumbleweed-setup/setup-scripts/05desktop
bash $HOME/git/tumbleweed-setup/setup-scripts/06editors
bash $HOME/git/tumbleweed-setup/setup-scripts/07opipkgs
bash $HOME/git/tumbleweed-setup/setup-scripts/08asus
bash $HOME/git/tumbleweed-setup/setup-scripts/09flatpak
bash $HOME/git/tumbleweed-setup/setup-scripts/10rustpkgs

echo "Installing Packages from Source"
sudo bash ~/tumbleweed-setup/source_builds/app2unit
bash ~/tumbleweed-setup/source_builds/Emacs
