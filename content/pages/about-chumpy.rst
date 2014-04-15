About Chumpy5000 
=================

:category: About
:slug: about-chumpy

Chump is an interactive IRC bot / web log generator. Our chumpy bot is 
chumpy5000, and our log is visible at `http://chump.chicagolug.org`_.

Post to Chumpy!
***************

To post to chumpy, just paste a link at the start of a line in the IRC channel
like so:

.. code-block:: text

       http://foo.com/bar.html

Chumpy will see the link, and assign it a letter (In this case, the letter "A")
like this:

.. code-block:: text

       | Notice(chumpy5000): A:
       | http://foo.com/bar.html from irc-username   

Use the letter (and a colon and a pipe) to give the link a title:

.. code-block:: text

       A:|Foo.com - home of all things fooish

Use the letter and a colon to add a comment to the link:

.. code-block:: text

       A:This is my comment about that foo.com page.
       
Add some emphasis to your comment:

.. code-block:: text
       
       A:This is my comment *with some bold text*.

You can even add a link to your comment:

.. code-block:: text

       A:This comment includes an [inline link to MediaGoblin|http://mediagoblin.org] because they are fooish.

You can add an image as a comment, too:

.. code-block:: text

       A:+[http://url.of.image.com/image.jpg]
       
If you want to say something, but don't want to create a link, create a BLURB:

.. code-block:: text

       BLURB:This is a blurb. A way to make a note without a link.

Correcting Mistakes
*******************

If you mess up, you can correct your post or comment by overwriting it:

.. code-block:: text

       A:http://foo.com/var-bar.html    (This will assign a new link to the letter "A")
       
       A1:This will replace the comment identified as "A1".

If you want to delete your original post altogether, just do this:

.. code-block:: text

       A:""

Getting Help
************

If you want a reminder about all of this, chump will answer requests for help
that you send it in the channel:

.. code-block:: text

       chumpy5000:help
       
       or

       chumpy5000:morehelp

That's about it. Have fun with chump!

.. _`http://chump.chicagolug.org`: http://chump.chicagolug.org
