#!/bin/bash
echo "Initial Setup"
sudo cp -R ~/tumbleweed-setup/preconfigured-files/zypp.conf /etc/zypp/
sudo cp -R ~/tumbleweed-setup/preconfigured-files/variables.sh /etc/profile.d/

sudo zypper ref
sudo zypper dup
sudo zypper ar -cfp 90 https://ftp.gwdg.de/pub/linux/misc/packman/suse/openSUSE_Tumbleweed/ packman
sudo zypper dup --from packman --allow-vendor-change
sudo zypper install flatpak opi curl wget
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

echo "Installing System Packages"
sleep 5
sudo zypper install upower lynis sysstat acct rng-tools haveged man man-pages tealdeer aa_base-extras acl attr bind-utils bzip2 cnf cpio gzip logrotate lsscsi net-p7zip psmisc sed tar wget wireless-tools xz unrar unzip zip zram-generator xf86-input-libinput xorg-x11-fonts-core xorg-x11-server xorg-x11-driver-video xinit xterm xkeyboard-config xauth xorg-x11-libX11-ccache kernel-source kernel-syms dkms libvdpau1 libva-utils Mesa-libva xf86-video-nv nvidia-video-G06 nvidia-driver-G06-kmp-default nvidia-gl-G06 nvidia-utils-G06 kernel-firmware-nvidia libglvnd libglvnd-devel kernel-firmware-amdgpu xf86-video-amdgpu ffnvcodec-devel   


echo "Intalling Desktop Environment"
sleep 5
sudo zypper install atuin bat btop cliphist emacs eza fastfetch file-roller fzf gnome-themes-extras gtk2-engine-murrine hyprland hypridle hyprlock hyprpaper imv kvantum-manager kvantum-qt5 kvantum-qt6 kvantum-themes kitty kitty-shell-integration kitty-terminfo lazygit mpv nwg-drawer nwg-look pyprland qt5ct qt6ct ripgrep rofi-wayland sassc starship stow tealdeer thunar thunar-archive-plugin thunar-media-tags-plugin thunar-volman tmux tuigreet xdg-desktop-portal-hyprland xwayland yazi zathura zathura-plugin-pdf-poppler zoxide zsh    

echo "Installing Python Packages"
sleep 5
sudo zypper in python313-base python313-black python313-flake8 python313-pip python313-pipx python313-pytest python313-requests python313-setuptools python313-tox python313-virtualenv python313-installer python313-build 

echo "Setting Up Editors"
sleep 5
sudo zypper in cargo emacs fd harfbuzz go google-noto-sans-symbols-fonts ImageMagick lua-language-server lua51 lua51-luarocks neovim npm nodejs python313-neovim ripgrep rust shfmt stix-fonts wl-clipboard xdg-user-dirs xdg-user-dirs-gtk yarn 

mkdir -p ~/.npm-global/lib
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
npm install -g neovim

echo "Installing Opi Packages"
sleep 5
opi codecs thefuck nerdfonts-JetBrainsMono nerdfonts-Ubuntu nvidia-vaapi-driver gtk4-layer-shell asusctl asusctl-rog-gui supergfxctl

echo "Setting Up Git"
sleep 5
sudo zypper in git-core git-credential-libsecret gnome-keyring subversion
git config --global user.name "aahsnr"
git config --global user.email "ahsanur041@proton.me"
git config --global credential.helper /usr/libexec/git/git-credential-libsecret

echo "Setting Up for ASUS Laptops"
sleep 5
sudo zypper ar --priority 50 --refresh https://download.opensuse.org/repositories/home:/luke_nukem:/asus/openSUSE_Tumbleweed/ asus-linux
sudo zypper rm tlp
sudo zypper rm suse-prime
sudo systemctl enable --now power-profiles-daemon.service supergfxd

