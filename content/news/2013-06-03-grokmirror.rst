Mirroring kernel.org repositories
=================================

:category: Site news

If you would like to mirror all or a subset of kernel.org git
repositories, please use a tool we wrote for this purpose, called
grokmirror. Grokmirror is git-aware and will create a complete mirror of
kernel.org repositories and keep them automatically updated with no
further involvement on your part.

Grokmirror works by keeping track of repositories being updated by
downloading and comparing the master manifest file. This file is only
downloaded if it's newer on the server, and only the repositories that
have changed will be updated via "git remote update".

You can read more about grokmirror by reading the README_ file.

.. _README: https://git.kernel.org/cgit/utils/grokmirror/grokmirror.git/tree/README.rst

Obtaining grokmirror
--------------------
If grokmirror is not yet packaged for your distribution, you can obtain
it from a git repository::

    git clone git://git.kernel.org/pub/scm/utils/grokmirror/grokmirror.git

In additon to git, you will need to install the following python
dependencies on your mirror server:

  * GitPython_

.. _GitPython: http://pypi.python.org/pypi/GitPython/

Setting up a kernel.org mirror
------------------------------
It is recommended that you create a dedicated "mirror" user that will
own all the content and run all the cron jobs. It is generally
discouraged to run this as user "root".

The default repos.conf already comes pre-configured for kernel.org. We
reproduce the minimal configuration here::

    [kernel.org]
    site = git://git.kernel.org
    manifest = http://git.kernel.org/manifest.js.gz
    default_owner = Grokmirror User
    #
    # Where are we going to put the mirror on our disk?
    toplevel = /var/lib/git/mirror
    #
    # Where do we store our own manifest? Usually in the toplevel.
    mymanifest = /var/lib/git/mirror/manifest.js.gz
    #
    # Where do we put the logs?
    log = /var/log/mirror/kernelorg.log
    #
    # Log level can be "info" or "debug"
    loglevel = info
    #
    # To prevent multiple grok-pull instances from running at the same
    # time, we first obtain an exclusive lock.
    lock = /var/lock/mirror/kernelorg.lock
    #
    # Use shell-globbing to list the repositories you would like to mirror.
    # If you want to mirror everything, just say "*". Separate multiple entries
    # with newline plus tab. Examples:
    #
    # mirror everything:
    #include = *
    #
    # mirror just the main kernel sources:
    #include = /pub/scm/linux/kernel/git/torvalds/linux.git
    #          /pub/scm/linux/kernel/git/stable/linux-stable.git
    #          /pub/scm/linux/kernel/git/next/linux-next.git
    #
    # mirror just git:
    #include = /pub/scm/git/*
    include = *
    #
    # This is processed after the include. If you want to exclude some specific
    # entries from an all-inclusive globbing above. E.g., to exclude all
    # linux-2.4 git sources:
    #exclude = */linux-2.4*
    exclude =

Install this configuration file anywhere that makes sense in your
environment. You'll need to make sure that the following directories (or
whatever you changed them to) are writable by the "mirror" user:

  * ``/var/lib/git/mirror``
  * ``/var/log/mirror``
  * ``/var/lock/mirror``

Mirroring kernel.org git repositories
-------------------------------------
Now all you need to do is to add a cronjob that will check the
kernel.org mirror for updates. The following entry in
``/etc/cron.d/grokmirror.cron`` will check the mirror every 5 minutes::

    # Run grok-pull every 5 minutes as "mirror" user
    */5 * * * * mirror /usr/bin/grok-pull -p -c /etc/grokmirror/repos.conf

(You will need to adjust the paths to the grok-pull command and to
repos.conf accordingly to reflect your environment.)

The initial run will take many hours to complete, as it will need to
download about 50 GB of data.

Mirroring a subset of repositories
----------------------------------
If you are only interested in carrying a subset of git repositories
instead of all of them, you are welcome to tweak the ``include`` and
``exclude`` parameters.
