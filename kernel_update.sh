#!/bin/bash

[[ -n "$DEBUG" ]] &&  set -x


# Variable
KERNEL_SRC=/usr/src
GRUB_CFG_FILE=/boot/grub2/grub.cfg
LOG=/var/log/kernel_update
DATE=$(date "+%d%m%Y")


function usage () {
  echo "USAGE : "
  echo "$0 target_kernek_version"
}

if [[ $# -ne 1 ]]
then
  usage
  exit 1
fi

target=$1

GETUID=$(id -u)
if [ ${GETUID=} -ne 0 ]
then
  echo "This script must be run as root"
  exit 10
fi


if [ ! -d $KERNEL_SRC/linux-$target ]
then
  echo "$KERNEL_SRC/linux-$target doesn't exist"
  exit 2
fi


if [ ! -d $KERNEL_SRC/linux ]
then
  echo "$KERNEL_SRC/linux doesn't exist"
  exit 3
fi

if [ ! -f $KERNEL_SRC/linux/.config ]
then
  echo "$KERNEL_SRC/linux.config doesn't exist"
  exit 4
fi

cp $KERNEL_SRC/linux/.config $KERNEL_SRC/linux-$target
if [ $? -ne 0 ]
then
  echo "Error : cannot copy config file"
  exit 5
else
  echo "Copy ok"
fi

rm $KERNEL_SRC/linux
if [ $? -ne 0 ]
then
  echo “Error : cannot remove old symbolic link”
  exit 4
else
  echo "symbolic link ok"
fi

ln -s $KERNEL_SRC/linux-$target $KERNEL_SRC/linux
if [ $? -ne 0 ]
then
  echo "Error : cannot create symbolic link"
  exit 4
else
  echo "symbolic link ok"
fi

cd $KERNEL_SRC/linux
pwd

################################################################################
# Choosing kernel options
################################################################################
make oldconfig
 
################################################################################
# Compile and install kernel
################################################################################
make && make modules_install
# 
cp arch/x86_64/boot/bzImage /boot/kernel-$target
if [ $? -ne 0 ]
then
  echo "Error : cannot copy kernel image to /boot"
  exit 5
else
  echo "Copy ok"
fi

################################################################################
# External modules : nvidia driver, virtual box ...
################################################################################
emerge -1 @module-rebuild
if [ $? -ne 0 ]
then
  echo "Error : cannot rebuild external kernel modules"
  exit 6
else
  echo "External kernel modules rebuilding ok"
fi

################################################################################
# Grub
################################################################################
# Backup
cp -p $GRUB_CFG_FILE $GRUB_CFG_FILE.$DATE
if [ $? -ne 0 ]
then
  echo "Error : cannot backup grub config file"
  exit 5
else
  echo "Copy ok"
fi

# Update grub config
grub-mkconfig -o $GRUB_CFG_FILE
if [ $? -ne 0 ]
then
  echo "Error : cannot update grub config"
  exit 7
else
 echo "Update ok"
fi

