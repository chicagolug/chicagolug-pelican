Coffee, Nefarious Actors and Virtual Private Networks
======================================================

:author: ChicagoLUG
:summary: ChicagoLUG's setup for OpenVPN. We've set it up, and here's how we did it.
:date: 2014-11-18 18:42
:category: News
:slug: news/2014-11-18-openvpn-at-chicagolug
:tags: VPN, OpenVPN, CentOS, Fedora, SELinux

Also Known As: OpenVPN via the ChicagoLUG
------------------------------------------

You're at the coffee shop and you are using their handy wifi. It's free! That's
great! It doesn't even require a password, which is so convenient! You can
totally surf the web while you sip your Americano, giving you plenty of
time to study with your friend who will be here in a few minutes. All is
excellent.

Except, that there is a person who is wearing a trenchcoat in the corner. They
are probably drinking decaf. And they are using Wireshark to sniff all of your
packets, reading your cookies and getting your passwords. Woe is you. This is
terrible. They are going to get all of your personal information and sell
it to a Russian mafioso.  That mafioso will use your credit card information to
purchase large quantities of ChapStick (do you know what the winter is like in
Russia?), and you'll have to pay for it.

.. image:: |filename|/images/trenchcoat_man.jpg
       :height: 768 px
       :width: 544 px
       :alt: Credit to Wikipedia Authors - https://en.wikipedia.org/wiki/Trench_coat
       :align: center

.. class:: center

       A nefarious hacker shows where he hides his stolen passwords.

What can you do? If only there was a way to establish a secure connection over
an insecure network. And if only there were instructions to help you set all of
it up. If only . . . 

Fortunately for you, there is something like that. It's amazing. It's right
here. We here at the ChicagoLUG have put together instructions on how to set
up a Virtual Private Network - both on the server end, and on the client end.
That's right.


Drink Americano. Surf the Internet. Don't Worry
-------------------------------------------------

In this post we'll learn how to set up our own `OpenVPN`_ server and connect to
it from our own computer. When we're done, we'll have a VPN setup that we can
access from coffee shops, hotels, conferences, and anywhere else where we want,
foiling the plans of trenchcoat-wearing decaf drinkers.

What will we use to do this?  Well, our VPN server is a CentOS 6.5 cloud-based
server, and we'll connect to it using GNOME's Network Manager on Fedora 20.
Yes, Linux all the way. 

What's the Catch? Really? How Can This Be Possible?
----------------------------------------------------

This post is lengthy enough as it is, so we'll assume that you've taken steps
to secure your server (e.g., that you disable root logins, have key-based
authentication, enabled SELinux, etc.). I mean, how can you expect to thwart
coniving mafiosos if you do not at least take these steps? If you do need
information on those topics, please do be in touch with us, though.

With that in mind,  we'll get straight to configuring our VPN server by
following these steps:

1. Install some basic software on our server and on our client workstation
2. Review the keys that we'll need to authenticate clients to servers
3. Create our OpenVPN certificates and keys
4. Set the OpenVPN server options
5. Set the client configuration options
6. Surf the internet

Install Needed Software and Set Up Directories
------------------------------------------------

We'll start by installing some software, and then we'll create and configure
our needed directories. With those items in place, we'll then set up our VPN
certificates and keys.

On the Server
**************

On the server we need to install *rsync* and the *epel-release* (`EPEL repository`_)
package, as well as the *openvpn* package. OpenVPN is in the EPEL repository,
so we need to make sure that EPEL is installed first:

.. code-block:: text
  
  # yum install rsync epel-release && yum install openvpn

On the Client
**************

On the Fedora client workstation, we just need to install *OpenVPN* and
*easy-rsa* packages:

.. code-block:: text

  # yum install yum install openvpn easy-rsa

The `easy-rsa`_ scripts are part of the OpenVPN project, and help us build and
maintain our keys.

Note that we will create the necessary certificates and keys from our
client workstation, and then transfer any needed keys to the server. *We*
*do not recommend generating the keys from the cloud server. The random*
*entropy in the cloud server's virtualized environment may not be random* 
*enough to guarantee safe keys*.

The easy-rsa scripts are stored in the */usr/share/easy-rsa/* directory by
default. We need to use them from the */etc/* directory, though, so we'll
create two subdirectories inside the /etc/openvpn directory, and then we'll
copy the scripts to that directory:

.. code-block:: text

  # mkdir -p /etc/openvpn/easy-rsa/keys
  # cp -avr /usr/share/easy-rsa/2.0/* /etc/openvpn/easy-rsa/

With those directories and scripts in place, let's move on to look at
certificates and keys.

What Keys and Certificates Do We Need? What Purpose Do They Serve?
-------------------------------------------------------------------

Although you can require VPN passwords, and even use hardware authentication
tokens when connecting a VPN, this guide will just use keys to
authenticate VPN clients with our VPN server.

Here are the keys that we're going to create as part of our VPN server:

* ca.crt      - The Root certificate, used to sign all keys. You should keep key this secure.
* server.crt  - Public key of the server
* server.key  - Private key of the server
* ta.key      - TLS-Auth key used to add an additional signature to the SSL/TLS handshake packets. This helps prevent denial-of-service attacks.
* dh4096.pem  - Diffie-Helman key used to create a secret, ephemeral key for each VPN session
* client.crt  - Public key of the client
* client.key  - Private key of the client

In the end, the ca.crt, server.crt, server.key, dh4096.pem and ta.key files
will reside on the server. The ca.crt, client.crt, client.key and ta.key
files will reside on the client.

The server and client certificates and keys are used to authenticate and
establish the initial connection between the client and server. The *ta.key*
assists in this process, adding one more layer of authentication to the initial
connection process.

Once that secure connection is established, the `Diffie-Hellman`_ certificate is
used to further encrypt the connection. While the client and server keys are
static, the encryption provided by the Diffie-Hellman certificate is
*ephemeral*, and the secret keys it generates are only used during that one
encrypted session. This provides `perfect forward secrecy`_. 

How Do We Create Our Keys?
----------------------------

Those are the keys, but how do we set them up? The keys that we create are
partly based on the values that we enter into a configuration file.
That configuration file is the *vars* file, and it ensures that our key values
are consistent across our various certificates and keys.

We'll edit the *vars* file now:

.. code-block:: text

  # cd /etc/openvpn/easy-rsa/
  # vi vars

Use your editor to review or update the key size, country, state, city,
email address, and other values to your desired values. Do not leave these
values blank:

.. code-block:: text

  [...]
  # Increase this to 2048 if you
  # are paranoid.  This will slow
  # down TLS negotiation performance
  # as well as the one-time DH parms
  # generation process.
  export KEY_SIZE=4096

  # In how many days should the root CA key expire?
  export CA_EXPIRE=3650   #10 years

  # In how many days should certificates expire?
  export KEY_EXPIRE=3650  #10 years

  # Don't leave any of these fields blank.
  export KEY_COUNTRY="US"
  export KEY_PROVINCE="Illinois"
  export KEY_CITY="Chicago"
  export KEY_ORG="ChicagoLUG"
  export KEY_EMAIL="user@email.com"
  export KEY_OU="server"
  [...]

You can save the file after editing these options.

You'll note that we've increased the key size beyond the recommended value.
OpenVPN supports a keysize of this length, and this key is only used to
establish the initial connection. That is, this key isn't used once the VPN
connection is active. So although it may increase the time it takes to
establish our connection, it does not impact browsing speed. Moreover, we've
used this key size in daily use for some time, and have not encountered any
issues with it.

Apparently, we're also very paranoid. Twice as paranoid as the noted level of
paranoia, apparently . . . *takes a sip of Americano and looks cautiously*
*around the room*.

Next, we'll copy over our chosen openssl configuration:

.. code-block:: text

  # cp -av openssl-1.0.0.cnf openssl.cnf

Then we'll tell the following processes to use the options from our *vars*
file:

.. code-block:: text

  # source ./vars

Building our Keys and Certificates
***********************************

With our key variables set, we'll now create the Certificate Authority (CA) key
and cert, as well as
our server keys and certificates. We'll start in the openvpn/easy-rsa
directory, and clear out any keys that may have already been in our keys
directory:

.. code-block:: text

  # ./clean-all

Our system is now fully prepped, and we're ready to start creating our keys.

The Primary Key: the Certificate Authority
------------------------------------------

We'll run this command to create the CA certificate and key. These are the
root certificate and key, and are used to sign the other certificates and
keys that we will create:

.. code-block:: text

  # ./build-ca

Here's what that will look like. You can press ENTER for each of the options:

.. code-block:: text

  Generating a 4096 bit RSA private key
  ...............................................................++
  ...........................................++
  writing new private key to 'ca.key'
  -----
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  -----
  Country Name (2 letter code) [US]:
  State or Province Name (full name) [IL]:
  Locality Name (eg, city) [Chicago]:
  Organization Name (eg, company) [ChicagoLUG]:
  Organizational Unit Name (eg, section) [server]:
  Common Name (eg, your name or your server's hostname) [ChicagoLUG CA]:
  Name [EasyRSA]:
  Email Address [user@email.com]:

Create the Server Keys
------------------------

We have now generated the CA certificate and CA key. We'll next create our 
server certificate and key:

.. code-block:: text

  # ./build-key-server server

Here's how that will look. You can see the process is very similar to creating
our CA certificate and key:

.. code-block:: text

  [root@openvpn easy-rsa]# ./build-key-server server
  Generating a 4096 bit RSA private key
  ......................++
  ..................++
  writing new private key to 'server.key'
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  Country Name (2 letter code) [US]:
  State or Province Name (full name) [IL]:
  Locality Name (eg, city) [Chicago]:
  Organization Name (eg, company) [ChicagoLUG]:
  Organizational Unit Name (eg, section) [Server]:
  Common Name (eg, your name or your server's hostname) [server]:
  Name [EasyRSA]:
  Email Address [user@email.com]:

  Please enter the following 'extra' attributes
  to be sent with your certificate request
  A challenge password []:
  An optional company name []:
  Using configuration from /etc/openvpn/easy-rsa/openssl-1.0.0.cnf
  Check that the request matches the signature
  Signature ok
  The Subject's Distinguished Name is as follows
  countryName           :PRINTABLE:'US'
  stateOrProvinceName   :PRINTABLE:'IL'
  localityName          :PRINTABLE:'Chicago'
  organizationName      :PRINTABLE:'ChicagoLUG'
  organizationalUnitName:PRINTABLE:'server'
  commonName            :PRINTABLE:'server'
  name                  :PRINTABLE:'EasyRSA'
  emailAddress          :IA5STRING:'user@email.com'
  Certificate is to be certified until May 10 12:50:13 2019 GMT (1825 days)
  Sign the certificate? [y/n]:y
  
  
  1 out of 1 certificate requests certified, commit? [y/n]y
  Write out database with 1 new entries
  Data Base Updated

Create the Client Certificate and Key
--------------------------------------

We'll create client certificates and keys with the following command:

.. code-block:: text

  # ./build-key client

If you want to create certificate and key files for more than one client, you
should replace the client parameter with an unique identifier (e.g., client0,
client1, client2, etc.).

Here's how this process looks:

.. code-block:: text

  Generating a 4096 bit RSA private key
  .......+++
  .....................+++
  writing new private key to 'client.key'
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  Country Name (2 letter code) [US]: 
  State or Province Name (full name) [IL]: 
  Locality Name (eg, city) [Chicago]: 
  Organization Name (eg, company) [ChicagoLUG]: 
  Organizational Unit Name (eg, section) [client]: 
  Common Name (eg, your name or your server's hostname) [client]: 
  Name [EasyRSA]: 
  Email Address [user@email.com]: 

  Please enter the following 'extra' attributes
  to be sent with your certificate request
  A challenge password []: 
  An optional company name []: 
  Using configuration from /etc/openvpn/easy-rsa/openssl-1.0.0.cnf
  Check that the request matches the signature
  Signature ok
  The Subject's Distinguished Name is as follows
  countryName           :PRINTABLE:'US'
  stateOrProvinceName   :PRINTABLE:'IL'
  localityName          :PRINTABLE:'Chicago'
  organizationName      :PRINTABLE:'ChicagoLUG'
  organizationalUnitName:PRINTABLE:'client'
  commonName            :PRINTABLE:'client'
  name                  :PRINTABLE:'EasyRSA'
  emailAddress          :IA5STRING:'user@email.com'
  Certificate is to be certified until May 08 12:21:42 2024 GMT (3650 days)
  Sign the certificate? [y/n]:y ----> Type Y and Press Enter

  1 out of 1 certificate requests certified, commit? [y/n]y ----> Type Y and Press Enter
  Write out database with 1 new entries
  Data Base Updated


Create Diffie Hellman Parameter
********************************

The Diffie Hellman key is what creates the shared secret key after the initial
connection has been established. This key is then used to encrypt the VPN
communications for that session.

We'll use this command to create the DH key:

.. code-block:: text

  # ./build-dh

Sample output:

.. code-block:: text

  Generating DH parameters, 4096 bit long safe prime, generator 2
  This is going to take a long time

And it does take a long time. Now would be a good time to sip some coffee
or clean off your desk. And then make some tea. And then drink it.

Create a TA key
****************

There's one more key that we need to create - a TA key so that we can use
OpenVPN's `TLS-Auth`_ feature. Using this feature adds an additional cryptographic
signature to our initial attempts to authenticate the client to the server.
If the server does not see this cryptographic signature included in the initial
connection attempt, it won't continue to validate the connection - thus preventing
denial-of-service attacks.

.. code-block:: text

  # openvpn --genkey --secret ta.key && mv ta.key keys/

You'll notice that, unlike our prior commands, we actually had to move the
ta.key file into the *keys* directory. 

We're done creating keys, though, and the necessary keys and certificates are now
present in our /etc/openvpn/easy-rsa/keys/ directory.

.. code-block:: text

    ca.crt
    dh4096.pem
    server.crt
    server.key
    ta.key

Go to the directory /etc/openvpn/easy-rsa/keys/ and enter the following command
to transfer the above files to /etc/openvpn/ directory.

.. code-block:: text

  # cd /etc/openvpn/easy-rsa/keys/
  # cp -avr dh4096.pem ca.crt server.crt server.key ta.key /etc/openvpn/

Moving the Server Keys to the Server
**************************************

Now we'll need to copy all server certificates and keys to the remote VPN
server. These are the keys that we'll need to copy to the VPN server:

.. code-block:: text

    ca.crt
    server.crt
    server.key
    dh4096.pem
    ta.key

Doing so can be a little tricky, though. Here's why. Look at the permissions of
the files below. Do you notice anything peculiar?

.. code-block:: text

  [root@openvpn keys]# ls -l | grep server
  -rw-r--r-- 1 root root 8083 Nov 11 12:53 server.crt
  -rw------- 1 root root 3272 Nov 11 12:53 server.key

You can see that the *server.key* file is only readable by root.
*(Note: This is also the same case for the ta.key file)*. Neither of them would
be picked-up by an rsync or scp transfer when those transfer processes are run
as a standard user.

You could use something like Ansible or SaltStack to transfer these files to
server in a more automated environment, but that's beyond the scope
of this article.

So, you can either use rsync over SSH as the root user (not recommended), or
you can temporarly change that file's permissions to be readable by other
users, move the files to a *non-root* user account, and transfer the files to
the server (where you'd reset the key permissions to the correct values).

As a note, you should never send your private keys to another person or user
via email. Moreover, do not back-up any keys without first encrypting them.

Here's how we can transfer the files via sftp, though:

.. code-block:: text
  
  $ echo "I am creating this directory as a non-root user on my client pc, aren't I? Let me make sure . . . : )"
  $ whoami
  $ echo "If entering 'whoami' displayed root, that is not what you want. Otherwise, create the directory below."
  $ mkdir ~/keys
  $ su    #switching to the root user
  # cd /etc/openvpn/easy-rsa/keys
  # chmod 644 server.key ta.key
  # cp -av ca.crt server.crt server.key ta.key /home/ - - $yourusername - - /keys

From the same client computer, you can then use this command to push up the
necessary files and reset their permissions:

.. code-block:: text

  $ echo "I am still on my client pc, aren't I? I should double check . . . : )"
  $ hostname
  $ echo "Hmm? Is that the hostname of my client pc? Ok. Cool."
  $ rsync -e "ssh -p $SERVER-SSH-PORT" -av ~/keys/ $serveruser@the.server.ip.address:/home/$serveruser/ 
  $ chmod 600 ~/keys/server.key ~/keys/ta.key & rm -rfi ~/keys  #this will set the permissions of the keys back to 600, then delete them 

After you push the files, you can go out to the server and set the permissions
back to their default state with these commands:

.. code-block:: text

  $ echo "I am on my server again, aren't I? Let me make sure . . . : )"
  $ hostname
  $ echo "That should be the hostname of my server. Sweet."
  $ cd ~/
  $ su
  # chmod 600 server.key ta.key   #this sets the proper file permissions
  # chown root:root server.key ta.key server.crt ca.crt #this sets the proper file ownership
  # mv server.key ta.key server.crt ca.crt /etc/openvpn/  #moves the files the proper directory

Congratulations. The keys are now set up on the client and server with the
proper permissions.

Configure the VPN Server
-------------------------

The certificates and keys are only part of the story, though. We need to
configure our server and client to use these keys to talk to each other. To do
this we need to create server and client OpenVPN configuration files. We'll
start on the server side.

Copy the server.conf file to /etc/openvpn/ directory:

.. code-block:: sh

  # cp -av /usr/share/doc/openvpn-2.3.2/sample/sample-config-files/server.conf /etc/openvpn/

Edit file server.conf,

.. code-block:: text

  vi /etc/openvpn/server.conf

Find and modify or uncomment the following lines to configure your OpenVPN
server:

.. code-block:: text

  [...]

  # Which TCP/UDP port should OpenVPN listen on?
  # If you want to run multiple OpenVPN instances
  # on the same machine, use a different port
  # number for each one.  You will need to
  # open up this port on your firewall.
  port 443
  
  # Note: We're using port 443 because that the is the SSL port on most
  # webservers. This will help us avoid issues with network firewalls.
  
  # TCP or UDP server?
  ;proto tcp
  proto udp

  # Substitute 2048 for 1024 if you are using
  # 2048 bit keys.
  # Note: We're using a 4096 bit key.
  dh dh4096.pem
  
  [...]
  
  push "redirect-gateway def1 bypass-dhcp"
  
  [...]

  # Also, uncomment and change the DNS servers to reflect your own DNS values.
  # Here I am using the OpenDNS public DNS servers.

  [...]
  
  push "dhcp-option DNS 208.67.222.222"
  push "dhcp-option DNS 208.67.220.220"
  
  [...]

  # For extra security beyond that provided
  # by SSL/TLS, create an "HMAC firewall"
  # to help block DoS attacks and UDP port flooding.
  # Generate with:
  #   openvpn --genkey --secret ta.key
  # The server and each client must have
  # a copy of this key.
  # The second parameter should be '0'
  # on the server and '1' on the clients.
  tls-auth ta.key 0 # This file is secret


  # Select a cryptographic cipher.
  # This config item must be copied to
  # the client config file as well.
  ;cipher BF-CBC        # Blowfish (default)
  ;cipher AES-128-CBC   # AES
  ;cipher DES-EDE3-CBC  # Triple-DES
  # We chose to use this one instead.
  cipher  AES-256-CBC   # AES

You should also uncomment the following lines:

.. code-block:: text

  [...]
  
  user nobody
  group nobody
  
  [...]

You can then save and close the file.

IP forwarding and routing Configuration
****************************************

There are a few more configuration changes that we need to make on our server
to allow VPN requests to flow from our client, through our server, and out to
the greater internetnet. For one, we need to allow packet forwarding. To do
that, we'll edit the sysctl.conf file:

.. code-block:: text

  # vi /etc/sysctl.conf

Add the following lines to enable IP forwarding:

.. code-block:: text

  # Controls IP packet forwarding
  net.ipv4.ip_forward = 1

Run the following command to apply the sysctl changes.

.. code-block:: text

  # sysctl -p

Adjust iptables to forward traffic through VPN properly.
*********************************************************

We also need to set the proper firewall settings. Enter the following commands
one by one:

.. code-block:: text

  # iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
  # iptables -A INPUT -p tcp --dport 443 -j ACCEPT
  # iptables -I INPUT 1 -p udp --dport 443 -j ACCEPT
  # iptables -A INPUT -i eth0 -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
  # iptables -A OUTPUT -o eth0 -p tcp --sport 443 -m state --state ESTABLISHED -j ACCEPT
  # iptables -I FORWARD -i eth0 -o tun0 -j ACCEPT
  # iptables -I FORWARD -i tun0 -o eth0 -j ACCEPT
  # iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
  # iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE

Save the iptables changes using these commands:

.. code-block:: text

  # service iptables save
  # service iptables restart

Additional Server-side Configuration
*************************************
Let's see if our openvpn service will start.

.. code-block:: text

  # service openvpn start     # command to start the openvpn service
  
If it won't start, it is likely due to SELinux complaining about us using a
non-standard port. You can verify this
by checking /var/log/audit/audit.log file. If you see messages like this:

.. code-block:: text

  type=AVC msg=audit(1416364068.146:361): avc:  denied  { name_bind } for  pid=1742 comm="openvpn" src=443 scontext=unconfined_u:system_r:openvpn_t:s0 

Then that is your culprit. You can allow OpenVPN on port 443 by entering these
commands:

.. code-block:: text

  # yum install policycoreutils-python    # this provides the audit2allow utility that we'll use in the next command
  # grep openvpn /var/log/audit/audit.log | audit2allow -M mypol
  # semodule -i mypol.pp

Now try turning OpenVPN back on:

.. code-block:: text

  # service openvpn start     # it should work this time
  # chkconfig openvpn on      # will set the openvpn service to run at boot


Check to Make Sure the tun0 Interface is created
*************************************************

Verify if VPN interface(tun0) is created using ifconfig command:

.. code-block:: text

  ifconfig

Sample output:

.. code-block:: text

  eth0      Link encap:Ethernet  HWaddr 08:00:27:46:36:62  
            inet addr:192.168.1.2  Bcast:192.168.1.255  Mask:255.255.255.0
            inet6 addr: fe80::a00:27ff:fe46:3662/64 Scope:Link
            UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
            RX packets:604 errors:0 dropped:0 overruns:0 frame:0
            TX packets:100 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:1000 
            RX bytes:44166 (43.1 KiB)  TX bytes:14434 (14.0 KiB)

  lo        Link encap:Local Loopback  
            inet addr:127.0.0.1  Mask:255.0.0.0
            inet6 addr: ::1/128 Scope:Host
            UP LOOPBACK RUNNING  MTU:16436  Metric:1
            RX packets:0 errors:0 dropped:0 overruns:0 frame:0
            TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:0 
            RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)

  tun0      Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  
            inet addr:10.8.0.1  P-t-P:10.8.0.2  Mask:255.255.255.255
            UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1500  Metric:1
            RX packets:0 errors:0 dropped:0 overruns:0 frame:0
            TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:100 
            RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)


At this time, we should have a working OpenVPN server. Next, let us move to
client side configuration.


Client Configuration
*********************

We'll need to copy and edit the client.conf file. I'm doing this on a Fedora
client, so here's how I would do this:

.. code-block:: text

  # cp /usr/share/doc/openvpn/sample/sample-config-files/client.conf /home/ - - $yourusername - - /keys/client.ovpn


You'll note that I've changed the file name to client.ovpn. The layout is the
same as client.conf, but because GNOME's Network Manager allows you to set up a
VPN client just by importing an OVPN file, this makes things a lot easier.

Here are the client.conf/client.ovpn settings that we've chosen to use:

.. code-block:: text

  $ vi /home/- - $yourusername -- /keys/client.ovpn

  client                          #hey, we're a client
  dev tun                         #specificies tun/tap routing as tun
  proto udp                       #identifies the protocol as udp 
  remote 192.861.1.1 443          #vpn server ip address and port. not our real ip address. :)
  resolv-retry infinite           #if hostname resolve fails for --remote, retry resolve for n seconds before failing
  nobind                          #do not bind to local address and port.
  ca /etc/openvpn/ca.crt          #location of ca certificate
  cert /etc/openvpn/client.crt    #location of client certificate
  key /etc/openvpn/client.key     #location of client key
  tls-auth /etc/openvpn/ta.key 1  #note the "1". this should be set to "0" on the server's config.
  user nobody                     #drop privileges
  group nobody                    #drop privileges
  persist-key                     #this allows keys to be reread as the "nobody" user
  ns-cert-type server             #ensures that the host they connect with is a designated server
  cipher AES-256-CBC              #cipher should match that of the server
  comp-lzo                        #compression settings
  verb 2                          #set verbosity. can be helpful to set to 3 when troubleshooting.


Save that file, set it's ownership as root and and move it into your
/etc/openvpn directory:

.. code-block:: text

  $sudo chown root:root client.ovpn && sudo mv client.ovpn /etc/openvpn/

Now you'll need to import your *client.ovpn* information into your
Network Manager settings.

* From the Activities Overview in GNOME Shell, type *settings*
* Select *Network* from the list of applets, and click the *Plus* sign to create a new network setting
* Select *VPN* from the list of options, and then click *Import from file . . ."*
* Navigate to where your client.ovpn file is located (/etc/openvpn/client.ovpn), and click *Open*.
* Give the VPN connection a name (e.g., The hostname of your VPN server)
* Review the imported settings and click *Apply*
* Select the menu from the *top bar*, select VPN, and then set the slider to *On*.

You should see a secure network icon light if you're able to connect.
That’s it. Now the VPN server and client are connected securely. Happy VPNing!

.. _OpenVPN: https://openvpn.net/
.. _EPEL repository: https://fedoraproject.org/wiki/EPEL
.. _Diffie-Hellman: https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
.. _easy-rsa: https://github.com/OpenVPN/easy-rsa
.. _perfect forward secrecy: https://en.wikipedia.org/wiki/Forward_secrecy
.. _TLS-Auth: https://community.openvpn.net/openvpn/wiki/Hardening
