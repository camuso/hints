Summary: Prarit's System Setup

Name:    prarit
Version: 4.4
Release: 0
Group:   Development/Libraries
License: GPL
Source0: prarit.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: vim-enhanced
URL: http://www.prarit.com
ExclusiveArch: noarch

%description
This RPM installs various system setup scripts and sets the system up
so that Prarit can use it.

%prep
%setup -q  -n prarit -a 0

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/root
install -m 644 bashrc %{buildroot}/root/.bashrc
install -m 644 gitconfig %{buildroot}/root/.gitconfig
mkdir -p %{buildroot}/etc
install -m 644 vimrc %{buildroot}/etc/
install -m 644 DIR_COLORS %{buildroot}/etc/
install -m 644 DIR_COLORS.xterm %{buildroot}/etc/
mkdir -p %{buildroot}/etc/yum.repos.d
install -m 644 dhclient-exit-hooks %{buildroot}/etc/dhclient-exit-hooks
mkdir -p %{buildroot}/etc/NetworkManager/dispatcher.d
install -m 755 99-prarit %{buildroot}/etc/NetworkManager/dispatcher.d/99-prarit
mkdir -p %{buildroot}/usr/sbin/
install -m 755 bootonce %{buildroot}/usr/sbin/
install -m 755 grub2-edit %{buildroot}/usr/sbin/
install -m 644 rpmmacros %{buildroot}/root/.rpmmacros

%clean
rm -rf %{buildroot}

%post
# create mountpoints
mkdir /bigpapi
mkdir /fedora
mkdir /curly
cat << EOF >> /etc/fstab
bigpapi.bos.redhat.com:/vol/engarchive2/redhat /bigpapi nfs defaults 0 0
bigpapi.bos.redhat.com:/vol/fedora/rawhide /fedora nfs defaults 0 0
storage.bos.redhat.com:/vol/engineering/devarchive/redhat /curly nfs defaults 0 0
EOF

mount -a

# First time do this.  In subsequent reboots this will be done by
# dhclient-exit-hooks
echo "search bos.redhat.com redhat.com lab.bos.redhat.com" >> /etc/resolv.conf

arch=`uname -p`

#
#
#  IA64 ... one day this will go away!
#
#

if [ $arch == "ia64" ]; then
sed 's/rhgb quiet/debug/' /boot/efi/efi/redhat/elilo.conf > /tmp/elilo.conf
rm -f /boot/efi/efi/redhat/elilo.conf
mv /tmp/elilo.conf /boot/efi/efi/redhat/elilo.conf

cat << EOF >> /boot/efi/efi/redhat/elilo.conf
image=vmlinuz
        label=install
        initrd=initrd.img
        read-only
        append=debug
EOF
fi

#
#
# grub v1 changes
#
#

if [ `echo $arch | grep '86'` ]; then
if [ -e /boot/grub/grub.conf ]; then

sed 's/rhgb quiet/debug printk.time=1 ignore_loglevel/' /boot/grub/grub.conf >
/tmp/grub.conf
rm -f /boot/grub/grub.conf
mv /tmp/grub.conf /boot/grub/grub.conf
cat << EOF >> /boot/grub/grub.conf
title install
        kernel /vmlinuz debug
        initrd /initrd.img
EOF

fi
fi

#
#
# grub2 changes
#
#

if [ `echo $arch | grep '86'` ]; then
if [ -e /boot/default/grub ]; then

oldcmdline=`cat /tmp/grub | grep CMDLINE_LINUX | awk -F "\"" ' { print $2 } '`
echo "GRUB_CMDLINE_LINUX=\"${oldcmdline} ignore_loglevel printk.time=1
console=tty0 console=ttyS0,115200n81\""

fi
fi

#
#
# RHEL5 epel ia64 and x86 repo setup
#
#

egrep 'release 5' /etc/redhat-release > /dev/null
if [ $? -eq 0 ]; then

if [ $arch != "ia64" ]; then
# include RHEL5 epel repo
cat << EOF >> /etc/yum.repos.d/epel5.repo
[epel]
name=Extra Packages for Enterprise Linux 5 - \$basearch
#baseurl=http://download.fedora.redhat.com/pub/epel/5/\$basearch
mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=epel-5&arch=\$basearch
failovermethod=priority
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL
EOF

else
cat << EOF >> /etc/yum.repos.d/ia64-git.repo
[ia64 git repo]
name=ia64-git-repo
baseurl=http://prarit2.usersys.redhat.com/rhel5-ia64-git/
enabled=1
gpgcheck=0
EOF

fi

#
#
# RHEL5 installtree.sh script
#
#

cat << EOF >> /tmp/installtree.sh
yum -y install git-core unifdef
cd /home; git clone git://git.app.eng.bos.redhat.com/rhel5/kernel.git
EOF
chmod a+x /tmp/installtree.sh

fi

#
#
# RHEL4 epel repo
#
#

egrep 'release 4' /etc/redhat-release > /dev/null
if [ $? -eq 0 ]; then
if [ $arch != "ia64" ]; then
# include RHEL4 epel repo
cat << EOF >> /etc/yum.repos.d/epel4.repo
[epel]
name=Extra Packages for Enterprise Linux 4 - \$basearch
#baseurl=http://download.fedoraproject.org/pub/epel/4/\$basearch
mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=epel-4&arch=\$basearch
failovermethod=priority
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL
EOF

else
cat << EOF >> /etc/yum.repos.d/git-ia64.repo
[ia64 git repo]
name=ia64-git-repo
baseurl=http://prarit2.usersys.redhat.com/rhel4-ia64-git/
enabled=1
gpgcheck=0
EOF

fi

#
#
# RHEL4 installtree script
#
#

cat << EOF >> /tmp/installtree.sh
yum -y install git-core xterm
cd /home; git clone git://git.app.eng.bos.redhat.com/rhel-4.git
EOF
chmod a+x /tmp/installtree.sh

fi

#
#
# RHEL6 installtree script
#
#

egrep 'release 6' /etc/redhat-release > /dev/null
if [ $? -eq 0 ]; then

# there is no ia64 in RHEL6
# create /tmp/installtree.sh for RHEL4 tree
cat << EOF >> /tmp/installtree.sh
yum -y install git-core gcc cscope patchutils rpm-build xmlto asciidoc
redhat-rpm-config hmaccalc elfutils-libelf-devel zlib-devel binutils-devel
newt-devel python-devel perl-ExtUtils-Embed xterm
cd /home; mkdir -p rhel6-lite; cd rhel6-lite; git init; git remote add origin
git://git.app.eng.bos.redhat.com/rhel6.git; git fetch origin
master:refs/remotes/master; git checkout -b master --track remotes/master
EOF
chmod a+x /tmp/installtree.sh

fi

#
#
# RHEL7 installtree script
#
#

egrep 'release 7' /etc/redhat-release > /dev/null
if [ $? -eq 0 ]; then
cat << EOF >> /tmp/installtree.sh
yum -y install git-core gcc cscope rpm-build redhat-rpm-config xmlto asciidoc
elfutils-devel zlib-devel binutils-devel newt-devel python-devel
perl-ExtUtils-Embed pciutils-devel gettext hmaccalc gnupg xterm make nfs-utils
bison gnupg
cd /home; git clone git://git.app.eng.bos.redhat.com/rhel7.git
EOF
chmod a+x /tmp/installtree.sh
fi

#
#
# Fedora installtree script
#
#

egrep 'Fedora' /etc/redhat-release > /dev/null
if [ $? -eq 0 ]; then
cat << EOF >> /tmp/installtree.sh
yum -y install git-core gcc cscope rpm-build redhat-rpm-config xmlto asciidoc
elfutils-devel zlib-devel binutils-devel newt-devel python-devel
perl-ExtUtils-Embed pciutils-devel gettext xterm make bison gnupg hmaccalc
cd /home; git clone git://git.app.eng.bos.redhat.com/linux.git
EOF
chmod a+x /tmp/installtree.sh
fi


# On some trees dracut includes *ALL* modules in the initramfs.  This takes a
# long time, so do a -H by default to do hostonly modules
if [ -e /etc/dracut.conf ]; then
echo 'hostonly="yes"' >> /etc/dracut.conf
fi


# output a nice message at the end of the install.

echo
"******************************************************************************"
echo " Fedora git tree: git://git.app.eng.bos.redhat.com/linux.git "
echo " RHEL 7 git tree: git://git.app.eng.bos.redhat.com/rhel7.git "
echo " RHEL 6 git tree: git://git.app.eng.bos.redhat.com/rhel6.git "
echo " RHEL 5 git tree: git://git.app.eng.bos.redhat.com/rhel5.git "
echo " RHEL 4 git tree: git://git.app.eng.bos.redhat.com/rhel-4.git "
echo " "
echo " "
echo " To install the rpms and tree for this distro, run /tmp/installtree.sh"
echo
"******************************************************************************"
%files
/root/.bashrc
/root/.gitconfig
/root/.rpmmacros
/etc/vimrc
/etc/DIR_COLORS
/etc/DIR_COLORS.xterm
/etc/dhclient-exit-hooks
/etc/NetworkManager/dispatcher.d/99-prarit
/usr/sbin/bootonce
/usr/sbin/grub2-edit

%changelog
* Mon Jun 04 2012 Prarit Bhargava <prarit@redhat.com> 4.4.0
- fixed Fedora and RHEL7 /tmp/installtree.sh scripts to be executable
* Mon Apr 30 2012 Prarit Bhargava <prarit@redhat.com> 4.3.0
- added printk.time=1
- hmaccalc bison gnupg for fedora and rhel7
- added new git addresses for git://git.app.eng.bos.redhat.com/
* Tue Mar 27 2012 Prarit Bhargava <prarit@redhat.com> 4.2.0
- added RHEL7 installtree.sh
* Tue Mar 13 2012 Prarit Bhargava <prarit@redhat.com> 4.1.0
- big changes to vimrc
- add xterm to all distros
- add make to fedora
* Tue Oct 11 2011 Prarit Bhargava <prarit@redhat.com> 3.2.0
- updated bootonce
- added .rpmmacros
* Tue Aug 16 2011 Prarit Bhargava <prarit@redhat.com> 3.1.0
- added bootonce
* Tue Jun 28 2011 Prarit Bhargava <prarit@redhat.com> 3.0.0
- added Fedora entry for installtree.sh
- added gcc and cscope to RHEL6 installtree.sh
* Fri Apr 29 2011 Prarit Bhargava <prarit@redhat.com> 2.8.0
- changed dzickus to jwilson
* Wed Dec 22 2010 Prarit Bhargava <prarit@redhat.com> 2.7.0
- added git-pstart, git-ppush, git-ppop
* Mon Nov 08 2010 Prarit Bhargava <prarit@redhat.com> 2.6.0
- added lite checkout for rhel6 git tree
* Tue Sep 21 2010 Prarit Bhargava <prarit@redhat.com> 2.5.0
- added .gitconfig
* Thu Feb 11 2010 Prarit Bhargava <prarit@redhat.com> 2.4.1
- added /etc/dracut.conf modification
* Tue Feb 02 2010 Prarit Bhargava <prarit@redhat.com> 2.4.0
- added /etc/NetworkManager/dispatcher.d script to resolve.conf entries
* Mon Aug 24 2009 Prarit Bhargava <prarit@redhat.com> 2.3.0
- added RHEL6 git entry
* Thu Feb 26 2009 Prarit Bhargava <prarit@redhat.com> 2.2.0
- added ia64 git repos on prarit2.usersys.redhat.com system
* Mon Dec 22 2008 Prarit Bhargava <prarit@redhat.com> 2.1.0
- added /tmp/installtree.sh script for automated git tree installs
* Mon Aug 25 2008 Prarit Bhargava <prarit@redhat.com> 2.0.0
- switched to noarch
* Mon Aug 25 2008 Prarit Bhargava <prarit@redhat.com> 1.0.13
- added epel repositories for git
- removed /prarit mountpoint
* Tue May 06 2008 Prarit Bhargava <prarit@redhat.com> 1.0.12
- added dhclient-exit-hooks to make .bos.redhat.com search persistent
* Mon May 05 2008 Prarit Bhargava <prarit@redhat.com> 1.0.11
- updated to .bos network
* Wed Mar 03 2008 Prarit Bhargava <prarit@redhat.com> 1.0.10
- updated rawhide mountpoint
- added new server, client, and virt repos for RHEL5
- removed prarit-* repos.  I never used them.
* Fri Jul 27 2007 Prarit Bhargava <prarit@redhat.com> 1.0.9
- added fedora mount point
* Tue May 08 2007 Prarit Bhargava <prarit@redhat.com> 1.0.8
- added Fedora Extras GPG key
* Sat Mar 31 2007 Prarit Bhargava <prarit@redhat.com> 1.0.7
- added repos for git, fedora-extras to be able to install git on a system
* Mon Mar 24 2007 Prarit Bhargava <prarit@redhat.com> 1.0.6
- added .boston.redhat.com to bigpapi and prarit mounts
* Wed Jan 24 2007 Prarit Bhargava <prarit@redhat.com> 1.0.5
- added bigpapi repo
- added install grub and elilo entries
* Tue Oct 05 2006 Prarit Bhargava <prarit@redhat.com> 1.0.4
- added curly mount
* Tue Oct 05 2006 Prarit Bhargava <prarit@redhat.com> 1.0.3
- fixed typo in non-ia64 arches
* Tue Oct 03 2006 Prarit Bhargava <prarit@redhat.com> 1.0.2
- added grub.conf mods
* Tue Sep 12 2006 Prarit Bhargava <prarit@redhat.com> 1.0.1
- added prarit:/home/prarit mount
- replace rhgb quiet with debug in elilo.conf
* Thu Aug 21 2006 Prarit Bhargava <prarit@redhat.com> 1.0.0
- initial release

