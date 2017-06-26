#! /bin/bash

ANSIBLE_CONFIG=cmi.conf ANSIBLE_HOSTS=cmi-inventory ansible-playbook --extra-vars @/opt/cord/build/genconfig/config.yml -v setup-cmi-playbook.yml
