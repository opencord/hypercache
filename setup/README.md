## Set up a new CDN

### CDN - headnode prep

1. Install AMC.qcow2 and CentOS-6-cdnnode-0.4.qcow2 to /opt/cord_profile/images/
2. nova flavor-create --is-public true m1.cdnnode auto 8192 120 4
3. run the deploy-cdn playbook:
    cd /opt/cord/orchestration/xos_services/hypercache/setup
    ansible-playbook -i /opt/cord/build/platform-install/inventory/head-localhost --extra-vars @/opt/cord/build/genconfig/config.yml deploy-cdn-playbook.yml
4. ensure private keys are in /opt/cord/orchestration/xos_services/hypercache/setup/private
5. Install ACT
       * sudo easy_install -Z auraclienttools-0.4.2_parguera-py2.7.egg 

### CDN - cmi setup

1. Wait for images (AMC, CentOS-6-cdnnode-0.4) to be loaded into glance (check glance image-list for status)
2. XOS UI: Add cmi and CentOS images to MyDeployment
3. Instantiate CMI instance in mysite_cdn_control
       * flavor: m1.cdnnode
       * image: AMC
4. edit group_vars/all
       * update cmi_compute_node, cmi_mgmt_ip
       * do not update cmi_private_key -- the public part is baked into the image
5. run the following playbook:
       ansible-playbook -i /opt/cord/build/platform-install/inventory/head-localhost --extra-vars @/opt/cord/build/genconfig/config.yml generate-inventory-playbook.yml
6. run setup-cmi.sh
       * this will SSH into the CMI and run setup, then modify some settings.
       * it may take a long time, 10-20 minutes or more
7. log into CMI (ssh-cmi.sh) and setup socat to attach the CMI to eth1
       * socat TCP-LISTEN:443,bind=172.27.0.9,reuseaddr,fork TCP4:10.6.1.196:443
8. setup port forwarding from prod VM to CMI:
       * ssh -L 0.0.0.0:3456:172.27.0.9:443 ubuntu@offbeat-pin
       * (note IP address of CMI Instance and use in place of 172.27.0.9)

### CDN - cdnnode setup

1. Instantiate cdnnode instance in mysite_cdn_nodes
       * flavor: m1.cdnnode
       * CentOS-6-cdnnode-0.4.img
2. Log into compute node and Attach disk
       * on cloudlab w/ supersized compute node:
           * virsh attach-disk <instance_name> /dev/vdb vdb --cache none
       * (make sure this disk wasn't used anywhere else!)
3. enroll the new node in the cdn
       * ansible-playbook -i "localhost," example-node-playbook.yaml
       * find the bootscript in /tmp
4. log into cdnnode VM
       * make sure default gateway is good (check public connectivity)
       * make sure arp table is good
       * make sure CMI is reachable from cdnnode
       * run takeover script that was created by the CMI 
       * (I suggest commenting out the final reboot -f, and make sure the rest of it worked right before rebooting)
       * Node will take a long time to install
5. log into cdnnode
       * to SSH into cdnnode, go into CMI, vserver coplc, cd /etc/planetlab, and use debug_ssh_key.rsa w/ root user
       * check default gateway
       * fix arp entry for default gateway

### CDN - request router setup

1. Instantiate request router instance in mysite_cdn_nodes
       * flavor: m1.cdnnode
       * CentOS-6-cdnnode-0.4.img
2. enroll the new rr in the cdn
       * ansible-playbook -i "localhost," example-rr-playbook.yaml
       * find the bootscript in /tmp
3. log into the request router VM
       * run the bootscript
       * (I suggest commenting out the final reboot -f, and make sure the rest of it worked right before rebooting)
       * Node will take a long time to install

### CDN - setup content

1. Run the following playbook:
       * ansible-playbook -i "localhost," example-content-playbook.yaml

### CDN - important notes

We manually edited synchronizers/vcpe/templates/dnsasq_safe_servers.j2 inside the vcpe synchronizer VM:

    # temporary for ONS demo
    address=/z.cdn.turner.com/207.141.192.134
    address=/cnn-vh.akamaihd.net/207.141.192.134

### Test Commands

* First, make sure the vSG is the only DNS server available in the test client. 
* Second, make sure cdn_enable bit is set in CordSubscriber object for your vSG.
* curl -L -vvvv http://downloads.onosproject.org/vm/onos-tutorial-1.1.0r220-ovf.zip > /dev/null
* curl -L -vvvv http://onlab.vicci.org/onos-videos/Nov-planning-day1/Day1+00+Bill+-+Community+Growth.mp4 > /dev/null
* curl -L -vvvv http://downloads.onosproject.org/release/onos-1.2.0.zip > /dev/null

## Restart CDN after power-down

To do...
test


## notes

socat TCP-LISTEN:443,bind=172.27.0.9,reuseaddr,fork TCP4:10.6.1.196:443 

ssh -L 0.0.0.0:3456:172.27.0.9:443 ubuntu@offbeat-pin
