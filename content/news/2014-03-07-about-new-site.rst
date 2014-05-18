Welcome to Our New Home!
========================

:author: Jim Campbell
:summary: We've updated the ChicagoLUG.org website. Learn how it's all put together, and how you can put it together, too.
:date: 2014-03-09 19:05
:category: News
:slug: news/2014-03-09-about-new-site
:tags: Website, Pelican, Git, Virtualenv

Welcome to the new ChicagoLUG.org. We've rebased this site on `Pelican`_, the
wonderful, Python-based static-site generator. In case you couldn't tell, this
site actually got it's start from the `kernel.org`_ website. We've made quite a
few adjustments, but if you look closely at kernel.org and then look back at
our site, some things may look familiar. So, thank you, `kernel.org folks`_!

Sisters Are Doing It For Themselves (And So Can We)
---------------------------------------------------

Because the site is new, we'd like to talk about how it's put together.
This will help folks contribute updates to the site such as blog posts,
meeting announcements, and perhaps even contribute some non-cat-related
photographs.

.. image:: |filename|/images/2014-03-07-no-cats.jpg
       :height: 480 px
       :width: 640 px
       :alt: Photo credit to Richard Humphrey - http://www.geograph.org.uk/photo/3313427
       :align: center

In later posts we'll go over how to add content to the site and publish the
site to the web. In this post we'll just focus on how to build and view the
site on our own computer, though.

So to build this site we'll need to:

1. Install some software (or at least make sure that some software is already installed)
2. Use *git* to download the chicagolug.org source
3. Set up and activate a Python virtual environment
4. Start up the local development server and view our local instance of the site

Install Some Software
*********************

We need to make sure that we have some base software installed before we can
perform more advanced tasks. Specifically, we'll need `git`_ which is used to
manage our source files, and `virtualenv`_, which is used to create isolated
environments for Python code.

If you're using *Fedora* or a *Red Hat*-based distribution, use this command:

.. code-block:: txt

    $ sudo yum install git-core python-devel python-virtualenv python-virtualenvwrapper

If you're using *Debian* or a *Debian*-based distribution (e.g., Ubuntu, Linux
Mint, etc.), use this command:

.. code-block:: txt

    $ sudo apt-get install git-core virtualenv virtualenvwrapper

That should do it.

Get the Source
**************

The next step is to grab the source files for the website. It's all available
on `github`_:

.. code-block:: txt

    $ git clone git@github.com:j1mc/chicagolug-pelican.git && cd chicagolug-pelican

This will download the source and then move us to the *chicagolug-pelican*
directory. 

Set Up A Python Virtual Environment
***********************************

We can now use the *virtualenv* software that we just installed to
create an isolated Python environment. This environment will hold all of the
*Pelican* code, keeping it separate from any Python packages in our
operating system:

.. code-block:: txt

    $ virtualenv venv
    
    $ source venv/bin/activate
    
    $ pip install pelican typogrify pygments beautifulsoup4 pillow

It will take a bit of time for the various Python packages (and their
dependencies) to get installed. Now might be a good time to take a sip or two
of coffee.

Fire Up The Development Server
******************************

Everything downloaded successfully? Great. Let's activate our development
server and have a look at a local version of the site.

The development server is very useful, because it will locally recompile the
site every time we save changes to the site's source code, even if we haven't
yet committed those changes.

.. code-block:: txt

    $ ./develop_server.sh start

This command will start the server, compile the site and make the site
available at the following URL:  http://localhost:8000

If you need to, you can restart or stop the development server by entering:

.. code-block:: txt

    $ ./develop_server.sh restart

or

.. code-block:: txt

    $ ./develop_server.sh stop


That Should Do It!
------------------

This should give you what you need to get started with the site. Later we'll
be looking at how to add content, and how to push our updates to the cloud
so that the site gets refreshed for the rest of the world to see.

Let us know if you run into any problems, or if you have any questions. Cheers!


.. _`Pelican`: http://getpelican.com
.. _`kernel.org`: https://kernel.org
.. _`kernel.org folks`: https://git.kernel.org/cgit/docs/kernel/website.git/
.. _`git`: http://git-scm.com/
.. _`github`: https://github.com/j1mc/chicagolug-pelican
.. _`virtualenv`: http://docs.python-guide.org/en/latest/dev/virtualenvs/
