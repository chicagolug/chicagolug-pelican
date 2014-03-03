Hello, World
============

:author: ChicagoLUG
:summary: Let's try out the bloggings
:date: 2014-01-26 11:05
:category: News
:tags: Testing

Greetings
---------

This is an example post to show how various formatting elements can be
entered when creating a blog entry.

Post Metadata
-------------

Blog posts should have the following metadata at the top of the article:

.. code-block:: text

    Hello, World
    ============

    :author: Bill Gates, Abe Lincoln, Mr T
    :summary: Include a full article summary, and put it all on one continuous line. What you type here will show as the post description on the post archive pages
    :date: YYYY-MM-DD HH:MM
    :category: News (all blog posts should be under this category)
    :tags: Tag One, Tag Two, Another Tag


Post Sections
-------------

Here's how you can enter different sections. Note that the *underline* elements
need to be as long as the heading text.

.. code-block:: text
    
    First-Level Section Heading
    ---------------------------
    
    Second-Level Section Heading
    ****************************

And here's an example of what the two types section headings look like:
    
First-Level Section Heading
---------------------------

Turnip greens yarrow ricebean rutabaga endive cauliflower sea lettuce kohlrabi
amaranth water spinach avocado daikon napa cabbage asparagus winter purslane. 
    
Second-Level Section Heading
****************************
Nori grape silver beet broccoli kombu beet greens fava bean potato quandong
celery. 

Formatting and such
-------------------

Let's try some code highlighting.

.. code-block:: XML

   <page xmlns="http://projectmallard.org/1.0/"
      type="topic" style="task"
      id="gedit-save-file">

    <info>
      <link type="guide" xref="gedit-files-basic" group="third"/>
      <revision pkgversion="3.8" date="2013-02-24" status="review"/>
      <credit type="author">
        <name>Jim Campbell</name>
        <email>jwcampbell@gmail.com</email>
      </credit>
      <credit type="editor">
        <name>Sindhu S</name>
        <email>sindhus@live.in</email>
      </credit>
      <include href="legal.xml" xmlns="http://www.w3.org/2001/XInclude"/>

    </info>

    <title>Save a file</title>
  
      <p>To save a file in <app>gedit</app>, click on the disk-drive icon with the
      word <gui style="button">Save</gui> next to it.  You may also select
      <guiseq><gui style="menu">File</gui>
      <gui style="menuitem">Save</gui></guiseq>, or just press
      <keyseq><key>Ctrl</key><key>S</key></keyseq>.</p> <p>If you are saving a
      new file, the <gui>Save File</gui> dialog will appear, and you can select a
      name for the file, as well as the directory where you would like the file
      to be saved.</p>

    </page>

What if we want to include a picture? We can do that, too.

.. code-block:: rst
    
    .. image:: |filename|/images/yyyy-mm-dd/name-of-file.png
           :height: xxx px
           :width: xxx px
           :alt: nice picture
           :align: center

We'll try putting the images into yyyy-mm-dd directories for each meeting. It
should help to keep things organized.
