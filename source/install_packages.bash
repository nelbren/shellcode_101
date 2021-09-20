#!/bin/bash
#
# install_packages.bash
#
# v0.0.1 - 2021-09-20 - nelbren@nelbren.com
#

inform_task() {
  case $2 in
    1) echo -e "\e[30;48;5;3m$1!\e[0m\e[K";;
    2) echo -e "\e[7;49;93m$1:\e[0m\e[K";;
    *) echo -en "\e[30;48;5;7m$1...\e[0m\e[K"
  esac
}

inform_and_exit() {
  if [ "$1" == "0" ]; then
    echo -e "\e[7;49;92mOK\e[0m\e[K"
  else
    echo -e "\e[1;48;5;1m$2\e[0m\e[K"
    exit $1
  fi
}

check_if_normal_user_running() {
  inform_task "Am I running as a 'normal' user?"
  [[ "$(id -u)" == "0" ]] && e=1 || e=0
  inform_and_exit $e "NO!"
}

sudo_test_access_to_user() {
  user=$USER
  inform_task "Let's test if the '$user' can run sudo"
  id=$(sudo id -u)
  inform_and_exit $id "Problem checking if user can access 'sudo'"
}

install_package() {
  package=$1
  inform_task "Is the '${package}' package installed?"
  if dpkg -s $package 2>/dev/null 1>&2 ; then
    inform_and_exit 0 ""
  else
    inform_task "NO" 1
    inform_task "Ok, no problem, i will install '${package}' package" 2
    sudo apt install -y $package
    inform_task "Is the '${package}' package installed?"
    if dpkg -s $package 2>/dev/null 1>&2 ; then
      inform_and_exit 0 ""
    else
      inform_and_exit $? "Problem installing ${package}!"
    fi
  fi
}

install_packages() {
  packages="gcc nasm gdb"
  for package in $packages; do
    install_package $package
  done
}

check_if_normal_user_running
sudo_test_access_to_user
install_packages
