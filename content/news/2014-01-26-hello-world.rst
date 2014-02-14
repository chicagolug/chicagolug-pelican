Hello, World
============

:author: ChicagoLUG
:summary: Let's try out the bloggings
:date: 2014-01-26 11:05
:category: News
:tags: Testing

Greetings
---------

This is just a test post to see how various formatting elements will be handled
by this flask-based blog. It's a flat-file blog, integrated into the rest of
our flask-based website. 

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
