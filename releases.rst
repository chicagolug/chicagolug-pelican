Active kernel releases
======================

:slug: releases
:category: Releases

There are several main categories into which kernel releases may fall:

Prepatch
    Prepatch or "RC" kernels are mainline kernel pre-releases that are
    mostly aimed at other kernel developers and Linux enthusiasts. They
    must be compiled from source and usually contain new features that
    must be tested before they can be put into a stable release.
    Prepatch kernels are maintained and released by Linus Torvalds.

Mainline
    Mainline tree is maintained by Linus Torvalds. It's the tree where
    all new features are introduced and where all the exciting new
    development happens. New mainline kernels are released every 2-3
    months.

Stable
    After each mainline kernel is released, it is considered "stable."
    Any bug fixes for a stable kernel are backported from the mainline
    tree and applied by a designated stable kernel maintainer. There are
    usually only a few bugfix kernel releases until next mainline kernel
    becomes available -- unless it is designated a "longterm maintenance
    kernel." Stable kernel updates are released on as-needed basis,
    usually 2-3 a month.

Longterm
    There are usually several "longterm maintenance" kernel releases
    provided for the purposes of backporting bugfixes for older kernel
    trees. Only important bugfixes are applied to such kernels and they
    don't usually see very frequent releases, especially for older
    trees.

.. table:: Longterm release kernels

    ======== ==================== ==================
    Version  Maintainer           Projected EOL
    ======== ==================== ==================
    2.6.32   Willy Tarreau        Mid-2014
    2.6.34   Paul Gortmaker       Mid-2013
    3.0      Greg Kroah-Hartman   Oct, 2013
    3.2      Ben Hutchings        2016
    3.4      Greg Kroah-Hartman   Oct, 2014
    ======== ==================== ==================

Distribution kernels
--------------------
Many Linux distributions provide their own "longterm maintenance"
kernels that may or may not be based on those maintained by kernel
developers. These kernel releases are not hosted at kernel.org and
kernel developers can provide no support for them.

It is easy to tell if you are running a distribution kernel. Unless you
downloaded, compiled and installed your own version of kernel from
kernel.org, you are running a distribution kernel. To find out the
version of your kernel, run `uname -r`::

    # uname -r
    3.7.5-201.fc18.x86_64

If you see anything at all after a dash, you are running a distribution
kernel. Please use the support channels offered by your distribution
vendor to obtain kernel support.
