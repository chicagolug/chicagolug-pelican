Hello, World
============

:author: ChicagoLUG
:summary: Let's try out the bloggings
:date: 2014-01-26 11:05
:category: News
:tags: Testing

This is an example post to show how various formatting elements can be
entered when creating a blog entry. If you're creating a blog post for the LUG,
this should give you enough to get you started.

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
    
Without that metadata, the blog post won't post at all. We'll all be sad.

Post Sections
-------------

Here's how you can enter different sections. Note that the *underline* elements
need to be as long as the heading text.

.. code-block:: text
    
    First-Level Section Heading
    ---------------------------
    
    Second-Level Section Heading
    ****************************

And here's an example of what the two types section headings actually look
like:
    
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

To create code blocks, insert the code-block directive. It looks like this:

.. code-block:: text

  .. code-block:: text

  Start it out with the two dots, a space, two colons, and then the type of
  code you're typing in to the post.
  
  Once you go back to non-indented text, the code-block will end. It will do
  it like magic. You barely have to do anything.

What if we want to include a picture? We can do that, too.

.. code-block:: rst
    
    .. image:: |filename|/images/name-of-file.png
           :height: xxx px
           :width: xxx px
           :alt: nice picture
           :align: center

And here's the picture.

.. image:: |filename|/images/mr-t-with-kittens.jpg
       :height: 500 px
       :width: 375 px
       :alt: Credit to Phil Denton - https://secure.flickr.com/photos/flyingsaab/5659208018/sizes/m/
       :align: center

.. class:: center

    Picture of Mr. T with Kittens. Credit to `Phil Denton`_.

.. _`Phil Denton`: https://secure.flickr.com/photos/flyingsaab/5659208018/sizes/m/
