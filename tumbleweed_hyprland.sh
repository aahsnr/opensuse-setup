#!/bin/bash

echo "@postinstall"
sudo zypper ref
sudo zypper dup
sudo zypper ar -cfp 90 https://ftp.gwdg.de/pub/linux/misc/packman/suse/openSUSE_Tumbleweed/ packman
sudo zypper dup --from packman --allow-vendor-change
sudo zypper install flatpak opi curl wget
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

echo "@patterns-base-minimal_base"
sleep 5
sudo zypper install branding-openSUSE filesystem openSUSE-build-key openSUSE-release staging-build-key install aaa_base bash ca-certificates-mozilla coreutils coreutils-systemd glibc libnss_usrfiles2 pam pam-config purge-kernels-service rpm system-user-nobody systemd util-linux NetworkManager busybox-static elfutils glibc-locale-base hostname iproute2 issue-generator lastlog2 pam_pwquality procps shadow system-group-wheel system-user-bin system-user-daemon terminfo time timezone wtmpdb gnome-keyring upower xdg-user-dirs xdg-user-dirs-gtk lynis sysstat acct rng-tools haveged man man-pages tealdeer aa_base-extras acl attr bind-utils bzip2 cifs-utils cnf cpio cpupower cryptsetup curl deltarpm diffutils dmidecode dosfstools file findutils fuse gawk gettext-runtime glibc-locale gpg2 gpm grep gzip hwdata hwinfo iputils irqbalance klogd kmod krb5 less logrotate lsscsi mcelog net-snmp netcat-openbsd netcfg numactl pam-config p7zip parted pciutils perl-Bootloader perl-base pinentry plymouth prctl procinfo psmisc screen sed setserial sg3_utils smartmontools smp_utils strace sudo suse-module-tools tar tnftp usbutils wget wireless-tools wol xz unrar unzip zip zram-generator xf86-input-libinput xorg-x11-fonts-core xorg-x11-server xorg-x11-driver-video xinit xterm xkeyboard-config dbus-1-x11 dialog fontconfig fonts-config fribidi ghostscript-x11 libdbus-glib-1-2 numlockx opensuse-welcome susepaste udev-configure-printer xauth xorg-x11-libX11-ccache fzf lsd git-core git-credential-libsecret go go-doc npm nodejs autoconf automake binutils bison cpp flex gawk gcc gettext-tools glibc-devel libtool m4 make patch zlib-devel binutils-devel fdupes gcc-c++ libstdc++-devel patch pkgconf-pkg-config subversion rust cargo shfmt lua-language-server lazygit fd ripgrep neovim wl-clipboard python312-neovim bc ctags diffstat indent kernel-source kernel-syms libelf-devel patchutils libnss_usrfiles2 netcfg rpm-build boost-devel boost-jam ltrace posix_cc swig valgrind osc quilt spec-cleaner python312-base python312-black python312-devel python312-flake8 python312-pip python312-pipx python312-pytest python312-requests python312-setuptools python312-tox python312-virtualenv python312-installer python312-build dkms libvdpau1 libva-utils libglvnd libglvnd-devel Mesa-libva xf86-video-nv nvidia-video-G06 nvidia-driver-G06-kmp-default nvidia-gl-G06 nvidia-utils-G06 kernel-firmware-nvidia kernel-devel make acpid libglvnd libglvnd-devel kernel-firmware-amdgpu xf86-video-amdgpu ffnvcodec-devel libva-devel kvantum-manager kvantum-qt5 kvantum-qt6 kvantum-themes qt5ct qt6ct gnome-themes-extras gtk2-engine-murrine sassc ImageMagick celluloid pavucontrol pamixer pipewire pipewire-alsa pipewire-pulseaudio gstreamer-plugin-pipewire wireplumber libnvidia-egl-wayland libqt5-qtwayland qt6-wayland grim slurp hypridle hyprland hyprland-wallpapers hyprpicker xdg-desktop-portal-gtk xdg-desktop-portal-hyprland xwayland wf-recorder scdoc mate-polkit nwg-look
sudo zypper si -d hyprland
opi codecs

echo "@asus"
sleep 5
sudo zypper ar --priority 50 --refresh https://download.opensuse.org/repositories/home:/luke_nukem:/asus/openSUSE_Tumbleweed/ asus-linux
sudo zypper rm tlp
sudo zypper rm suse-prime
sudo zypper in asusctl supergfxctl asusctl-rog-gui power-profiles-daemon
sudo systemctl enable --now power-profiles-daemon.service supergfxd

echo "@chrome"
sleep 5
cd
sudo zypper addrepo https://dl.google.com/linux/chrome/rpm/stable/x86_64 google-chrome
sudo zypper repos
sudo zypper modifyrepo --refresh 1
wget https://dl.google.com/linux/linux_signing_key.pub
sudo rpm --import linux_signing_key.pub
sudo rm -rf linux_signing_key.pub
sudo zypper install google-chrome-stable

echo "@brave"
sudo zypper install curl
sudo rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc
sudo zypper addrepo https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo
sudo zypper install brave-browser

curl -fsSL https://bun.sh/install | bash &&
  sudo ln -s $HOME/.bun/bin/bun /usr/local/bin/bun

#sudo zypper install alacritty alacritty-zsh-completion kitty kitty-shell-integration kitty-terminfo thunar thunar-volman thunar-plugin-archive thunar-plugin-dropbox thunar-plugin-media-tags file-roller deluge xournalpp zathura zathura-plugin-pdf-poppler zathura-zsh-completion ranger bitwarden

echo "@npm"
sleep 5
cd && mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
npm install -g sass
cargo install matugen

go install go.senan.xyz/cliphist@latest

echo "@dots"
sleep 5
sudo rm -R $HOME/.local
sudo rm -R $HOME/.config/
cd && mkdir $HOME/.config
mkdir -p $HOME/.local/bin
ln -s $HOME/.dots/.config/alacritty $HOME/.config/
ln -s $HOME/.dots/.config/kitty $HOME/.config/
ln -s $HOME/.dots/.config/anyrun $HOME/.config/
ln -s $HOME/.dots/.config/btop $HOME/.config
ln -s $HOME/.dots/.config/gtk-3.0 $HOME/.config/
ln -s $HOME/.dots/.config/gtk-4.0 $HOME/.config/
ln -s $HOME/.dots/.config/hypr $HOME/.config/
ln -s $HOME/.dots/.config/Kvantum $HOME/.config/
ln -s $HOME/.dots/.config/lazygit $HOME/.config/
ln -s $HOME/.dots/.config/lsd $HOME/.config/
ln -s $HOME/.dots/.config/Thunar $HOME/.config/
ln -s $HOME/.dots/.config/qt5ct $HOME/.config/
ln -s $HOME/.dots/.config/qt6ct $HOME/.config/
ln -s $HOME/.dots/.config/wallpapers $HOME/.config/
ln -s $HOME/.dots/.config/waybar $HOME/.config/
ln -s $HOME/.dots/.local/bin/hypr $HOME/.local/bin
ln -s $HOME/.dots/.config/zathura $HOME/.config/
ln -s $HOME/.dots/.config/zsh $HOME/.config/
ln -s $HOME/.dots/.config/starship.toml $HOME/.config/
ln -s $HOME/.dots/.gtkrc-2.0 $HOME/
ln -s $HOME/.dots/.themes $HOME/
ln -s $HOME/.dots/.fonts $HOME/
ln -s $HOME/.dots/org $HOME/

echo "@systemd"
sleep 5
sudo systemctl set-default graphical.target
systemctl --user enable --now wireplumber.service pipewire-pulse.socket pipewire.socket pipewire-pulse.service pipewire.service pipewire-pulse.socket pipewire.socket pipewire-pulse.service pipewire.service

echo "@nvim-init"
sleep 5
ln -s $HOME/.dots/.config/nvim $HOME/.config/

echo "@zsh"
sleep 5
cd && curl -fsSL https://fnm.vercel.app/install | sh
zsh <(curl -s https://raw.githubusercontent.com/zap-zsh/zap/master/install.zsh) --branch release-v1
rm -R .zshrc
ln -s $HOME/.dots/.zshrc ~/
chsh -s $(which zsh)

echo "@git"
sleep 5
sudo cp -R ~/.dots/variables.sh /etc/profile.d/
git config --global user.name "zielOS"
git config --global user.email "ahsanur041@gmail.com"
git config --global credential.helper /usr/libexec/git/git-credential-libsecret

echo "@pipx"
pipx install hyprshade pyprland
