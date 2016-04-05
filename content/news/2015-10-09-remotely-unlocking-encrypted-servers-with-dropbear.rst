Remotely Unlocking Encrypted Servers with Dropbear (on Ubuntu)
===============================================================
:author: Joel Luelwitz
:summary: Remotely Unlocking Encrypted Servers with Dropbear (on Ubuntu).
:date: 2015-10-09 21:45
:category: News
:slug: news/2015-10-09-remotely-unlock-encrypted-server-with-dropbear
:tags: Encryption, Dropbear, Joel Luellwitz

Ever since Edward Snowden blew the whistle on the NSA's dragnet
surveillance, it has become apparent that we cannot depend on the
government to defend our 4th amendment right to privacy. I personally
felt a great sense of violation from the NSA's spying program and a few
months after the initial disclosures, it had not gone away. While I
cannot completely hide from surveillance, I certainly have the technical
aptitude to do something about it.

On my journey to hide my data from prying eyes, I have turned to
encryption with full disk encryption being one of several forms of
encryption that I use. Full disk encryption is relatively simple to
implement on a laptop, especially if you have a single hard drive. The
Ubuntu installer works great for setting this up. However, maintaining
an encrypted server is a bit more difficult. Problems arise when dealing
will power-loss and rebooting after system security updates.
Fortunately, most of these issues can be dealt with by installing
Dropbear and adding a couple custom scripts. What I am going to
demonstrate below is how you can SSH login to your initial boot
environment and remotely enter your disk encryption passphrase. From
here, your server will boot as usual but without you having to be
physically present.

Dropbear is a minimal SSH server (and client) designed for use on
embedded systems. Its small disk footprint makes it ideal for inclusion
in the initramfs (the initial boot filesystem). If you have an encrypted
server and Dropbear installed, Dropbear will be included in your
initramfs by default (which is kind of concerning from a security
perspective). You can install Dropbear with the following command on
your server:

.. code-block:: text

    tux@chicagolug$ sudo apt-get install dropbear

During installation, Dropbear will generate key pairs that are used for
login. Unfortunately, these asymmetric keys are only 1024 bits which are
too short by today's standards. The commands below delete most of the
1024 bit keys and generates replacement 4096 bit RSA keys:

.. code-block:: text

    tux@chicagolug$ cd /etc/dropbear/
    tux@chicagolug$ sudo rm dropbear_dss_host_key
    tux@chicagolug$ sudo rm dropbear_rsa_host_key
    tux@chicagolug$ sudo dropbearkey -t rsa -s 4096 -f dropbear_rsa_host_key
    tux@chicagolug$ sudo rm /etc/initramfs-tools/etc/dropbear/dropbear_rsa_host_key
    tux@chicagolug$ sudo dropbearkey -t rsa -s 4096 -f \
      /etc/initramfs-tools/etc/dropbear/dropbear_rsa_host_key

The keys in ``/etc/dropbear/`` are used to SSH login to the fully booted
system and the keys in ``/etc/initramfs-tools/etc/dropbear/`` are used to
SSH login into the initial RAM disk environment. DSA keys are limited to
1024 bits, so we just delete the ``/etc/dropbear/dropbear_dss_host_key``.
We leave the ``/etc/initramfs-tools/etc/dropbear/dropbear_dss_host_key``
alone because it will be regenerated the next time the initramfs is
rebuilt. We will mitigate this later.

To prevent falling victim to a man-in-the-middle attack, record the SSH
key fingerprints that where printed to the screen when you created the
keys. You will verify these fingerprints the first time you remotely
login. If you need to obtain them later, you can print the fingerprints
with the following command:

.. code-block:: text

    tux@chicagolug$ sudo dropbearkey -y -f <keyfile>

Now restart Dropbear so the new RSA key takes effect:

.. code-block:: text

    tux@chicagolug$ sudo service dropbear restart

We are going to use public key authentication to login to the initial
boot environment. We do this to avoid creating a password hash that, if
compromised, could potentially be cracked by an adversary. On your
workstation (**not** the server you just installed Dropbear on), create an
SSH key pair by entering:

.. code-block:: text

    tux@workstation$ ssh-keygen -t rsa -b 4096

Be sure to set a sufficiently long and complex passphrase. Anything less
than 16 characters is too short.

To allow for passwordless (but not passphraseless) login, use the
ssh-copy-id program to copy your public key to the ``~/.ssh/known_hosts``
file on the server. For this example, ``tux`` is the username and
``chicagolug.com`` is the server hostname. Of course you'll use your own
username and hostname (or IP address) here.

.. code-block:: text

    tux@workstation$ ssh-copy-id tux@chicagolug.org

At this point, we can disable SSH password logins. On the server, edit the
``/etc/default/dropbear`` file and add the ``-s`` argument to the
DROPBEAR_EXTRA_ARGS property. (This step is optional.)

.. code-block:: text

    DROPBEAR_EXTRA_ARGS=-s

Again, restart Dropbear so the new argument takes effect:

.. code-block:: text

    tux@chicagolug$ sudo service dropbear restart

Oddly, during installation Dropbear generates its own private keys for
you to copy onto your workstation. These keys are intended to be used
for remote authentication while the server is at the disk unlock screen.
This seems kinda fishy to me. Traditionally your private keys should
never leave the computer they are generated on, so I just delete the
Dropbear generated ones and use the same key we generated above. You can
delete the auto generated keys by issuing the following command:

.. code-block:: text

    tux@chicagolug$ sudo bash -c "rm /etc/initramfs-tools/root/.ssh/*"

Note that the actual ``rm`` command is a bash parameter because the shell
expansion will not work as a non-root user. This is because ``tux`` does
not have read access to ``/etc/initramfs-tools/root/.ssh/``.

Now copy your authorized_keys file to the .ssh directory within the
initramfs configuration directory. This will allow you to unlock the
server's hard disk from any of your computers that can currently perform
a passwordless login.

.. code-block:: text

    tux@chicagolug$ sudo cp ~/.ssh/authorized_keys \
      /etc/initramfs-tools/root/.ssh/authorized_keys

Now update your initramfs:

.. code-block:: text

    tux@chicagolug$ sudo update-initramfs -u

At this point you should be able to reboot your server and connect via
SSH while still at the disk unlock prompt. However, since the initramfs
instance of Dropbear uses a different private key than the post-boot
Dropbear instance, you'll get the following error:

.. code-block:: text

    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
    Someone could be eavesdropping on you right now (man-in-the-middle attack)!
    It is also possible that a host key has just been changed.
    The fingerprint for the RSA key sent by the remote host is
    89:f2:01:5f:e8:bb:34:e3:de:86:c6:3f:6c:27:b8:4d.
    Please contact your system administrator.
    Add correct host key in /home/lug/.ssh/known_hosts to get rid of this message.
    Offending RSA key in /home/lug/.ssh/known_hosts:1
      remove with: ssh-keygen -f "/home/lug/.ssh/known_hosts" -R chicagolug.com
    RSA host key for chicagolug.com has changed and you have requested strict
    checking.
    Host key verification failed.


To resolve this issue, we'll create two custom SSH host specifications.
On the workstation, open ``~/.ssh/config``, and enter the following:

.. code-block:: text

    Host chicagolug
        User tux
        Hostname chicagolug.com
        Port 22
        UserKnownHostsFile=~/.ssh/chicagolug-known_hosts

    Host chicagolug-boot
        User root
        Hostname chicagolug.com
        Port 22
        UserKnownHostsFile=~/.ssh/chicagolug-boot-known_hosts

Of course, replace the username and hostnames with values that match
your system.

To remotely login to the boot environment, type in the following:

.. code-block:: text

    tux@workstation$ ssh chicagolug-boot

You will be prompted to enter your passphrase and should receive the
root prompt. From here you can enter the commands to unlock your root
partition. Unfortunately, Ubuntu itself does not provide an easy way to
unlock the hard disk from this point forward. To unlock the root
partition, we have to shutdown Plymouth (Ubuntu's graphical splash
screen), run ``/scripts/local-top/cryptroot``, and kill ``askpass`` or ``/bin/sh``.
When typed by hand, this can easily turn into half a dozen commands and
can take a minute or so to execute. To speed up this process, I wrote
the following script:

.. code-block:: text

    #!/bin/sh
 
    # Quit the Ubuntu graphical splash screen. This is necessary for cryptroot
    #   to work right. The server will fall back to a non-graphical unlock
    #   screen.
    plymouth --quit    
    count=0
    # Looping gives us some control over the number of unlock attempts.
    while ! ( ls /dev/mapper/ | grep root > /dev/null ); do
        if [ $count -gt 0 ]; then    
            exit 1
        fi
        sleep 3
        count=$(( count + 1 ))
        # This script detects your encryption and LVM configuration and
        # prompts the user to unlock their encrypted hard disks.
        /scripts/local-top/cryptroot
    done
    # Kill these programs to keep 'init' moving.
    if ( ps | grep cryptsetup | grep askpass > /dev/null ); then
        kill -9 $(ps | grep cryptsetup | grep askpass | awk '{print $1}')
    fi
    if ( ps | grep /bin/sh | grep "sh -i" > /dev/null ); then
        kill -9 $(ps | grep /bin/sh | grep "sh -i" | awk '{print $1}')
    fi

Note that cryptroot was not necessarily intended to be thread safe, but I do
not see anything in it that makes a second concurrent instance of it unsafe.
The cryptroot script does a lot configuration detection work, so I still
recommend using it.

Back in the booted server environment, you should save this script to
``/usr/local/share/dropbear-unlock/dropbear-unlock``. Be sure to create any missing
directories. The script below will create an initramfs hook to add the
dropbear-unlock script to every initramfs installed on your system.

.. code-block:: text

    #!/bin/sh

    # These next few lines are used for dependency management. This ensures the
    #   'dropbear' hook has run before this one.
    PREREQ="dropbear"

    prereqs() {
        echo "$PREREQ"
    }

    case "$1" in
        prereqs)
            prereqs        
            exit 0
        ;;
    esac

    # Import the initramfs configuration and common routines
    . "${CONFDIR}/initramfs.conf"    
    . /usr/share/initramfs-tools/hook-functions

    # Install dropbear-unlock if cryptroot is setup and dropbear is not explicitly
    #   disabled
    if ( [ "${DROPBEAR}" != "n" ] && [ -r "/etc/crypttab" ] ); then
        if [ ! -x "/usr/sbin/dropbear" ]; then
            if [ "${DROPBEAR}" = "y" ]; then
                echo "dropbear_unlock_hook: FAILURE: Dropbear not found! Not"
                echo "  installing dropbear-unlock."
            else
                echo "dropbear_unlock_hook: WARNING: Dropbear not found. Not"
                echo "  installing dropbear-unlock."
            fi
        else
            if [ "$(sed '/^$/d;/^#/d' "/etc/crypttab" | wc -l)" = "0" ]; then
                echo "dropbear_unlock_hook: NOTICE: Skipping dropbear-unlock"
                echo "  installation because /etc/crypttab has no entries."
                exit 0
            fi
            if [ -x "${DESTDIR}/sbin/dropbear-unlock" ]; then
                echo "Script dropbear-unlock already exists."
                exit 0
            fi
            echo '/sbin/dropbear-unlock' >> "${DESTDIR}/etc/shells"
            rm -f "${DESTDIR}/sbin/dropbear-unlock"
            cp '/usr/local/share/dropbear-unlock/dropbear-unlock' \
                "${DESTDIR}/sbin/"
            chmod +x "${DESTDIR}/sbin/dropbear-unlock"
            # Typically we will not be using NSS, so we do not need to have
            #   support for special entries in the /etc/passwd file. Removing
            #   the config entry that the dropbear hook added.
            if [ -x "${DESTDIR}/etc/nsswitch.conf" ]; then
                rm -f "${DESTDIR}/etc/nsswitch.conf"
            fi
            echo "root:x:0:0:root:/root:/sbin/dropbear-unlock" > \
                "${DESTDIR}/etc/passwd"
            rm "${DESTDIR}/etc/dropbear/dropbear_dss_host_key"
        fi
    fi

(Credit: This code is based off of the Dropbear hook.)

Save this file as ``/etc/initramfs-tools/hooks/dropbear_unlock_hook`` and
make it executable.

.. code-block:: text

    tux@chicagolug$ sudo chmod a+x /etc/initramfs-tools/hooks/dropbear_unlock_hook

I have security concerns with Dropbear providing me with a root shell prompt
when I login to the initial boot environment. To resolve this issue, the hook
script makes the dropbear-unlock script the default root shell. As a security
feature, by default Dropbear will ignore the ``/etc/passwd`` shell entry for
'root' unless the shell is listed in ``/etc/shells``. Hence, the hook script also
adds dropbear-unlock to ``/etc/shells``. For some unknown reason, the dropbear hook
adds an option that allows NSS special entries in ``/etc/passwd``. I don't see any
good reason for this to be there, so I added a line to remove it. Remove my
``rm`` line if you find NSS special entries useful.

Above I mentioned that the Dropbear DSA key is regenerated each time a new
initramfs is built. The last ``rm`` line of the above script removes this key
after is it copied to the initramfs build directory. Since the DSA key still
exists in the source directory, it does not get regenerated.

The last thing we need to do is update the initramfs so that the
dropbear-unlock script is included:

.. code-block:: text

    tux@chicagolug$ sudo update-initramfs -u

At this point, try rebooting your server to verify you can login remotely.

.. code-block:: text

    tux@workstation:~$ ssh chicagolug-boot
    Enter passphrase for key '/home/tux/.ssh/id_rsa':
    /scripts/local-top/cryptroot: line 1: modprobe: not found
    Unlocking the disk
    /dev/disk/by-uuid/1d4f7fa8-dfc5-49d3-b836-d9af6096ea81 (sda5_crypt)
    Enter passphrase:
        Reading all physical volumes.  This may take a while...
        Found volume group "ubuntu-vg" using metadata type lvm2
        2 logical volume(s) in volume group "ubuntu-vg" now active
    /scripts/local-top/cryptroot: line 1: can't open /dev/mapper/ubuntu--vg-root: no such file
    cryptsetup: sda5_crypt set up successfully
    Connection to localhost closed.
    tux@workstation:~$ ssh chicagolug 
    Enter passphrase for key '/home/tux/.ssh/id_rsa':
    tux@chicagolug:~$

You might have noticed that there are a couple of errors in the above
output. However, everything still works as expected.

There is one more thing we can do to make this process work a little
better. If an error occurs early in the boot process and the system
restarts, by default Grub will wait indefinitely for the user to select
a boot option. Force grub to timeout in this scenario by adding the
following to ``/etc/default/grub``:

.. code-block:: text

    GRUB_RECORDFAIL_TIMEOUT=10

Now make the new setting take effect:

.. code-block:: text

    tux@chicagolug$ sudo update-grub

Now, I would like to spend a moment to address some security concerns you might
have with remote disk unlocking. One might point out that this whole process is
compromised if someone changes your public key or adds a key logger while you
are away. However, unless you plan on never leaving your computer, traditional
disk unlocking also relies on the assumption that no one can get physical
access to your computer. You might also have concerns about having your server
listening on a port while at the unlock prompt. While having an open port does
create another attack vector, once your server boots there will probably be an
open SSH port anyway. There is one legitimate security concern however.
Dropbear is a newer SSH server than OpenSSH. It is reasonable to assume that
less eyes have reviewed the Dropbear code and thus might be more likely to have
security holes. In my opinion, the added security of having full disk
encryption outweighs any risk of Dropbear having a critical vulnerability.

So that is about it. You should now be able to remotely unlock your encrypted
hard disk from anywhere you have an Internet connection. However, wouldn't it
be nice (and more secure) if your server with full disk encryption could
perform unattended security upgrades? In my next blog post, I'll explain how
this is possible!
