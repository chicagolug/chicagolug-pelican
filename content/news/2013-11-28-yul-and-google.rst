New frontend and googlesource.com
=================================

:category: Site news
:author: Konstantin Ryabitsev

Montreal fontend
----------------
We have added another official frontend for serving the kernel content,
courtesy of `Vexxhost, Inc`_. There is now a total of three frontends,
one in Palo Alto, California, one in Portland, Oregon, and one in
Montreal, Quebec. This should allow for better geographic dispersion of
official mirrors, as well as better fault tolerance.

Kernel.googlesource.com
-----------------------
We are happy to announce that kernel.googlesource.com is now relying on
grokmirror manifest data to efficiently mirror git.kernel.org, which
means that if accessing git.kernel.org is too high latency for you due
to your geographical location (EMEA, APAC), kernel.googlesource.com
should provide you with a fast local mirror that is at most 5 minutes
behind official sources.

We extend our thanks to Google for making this available to all kernel
hackers and enthusiasts worldwide.

TLS 1.2 and PFS
---------------
With the latest round of upgrades, we are now serving TLS 1.2 with PFS
across all kernel.org sites, offering higher protection against
eavesdropping.


.. _`Vexxhost, Inc`: http://vexxhost.com
