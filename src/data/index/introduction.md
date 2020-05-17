---

image: "cherry1.jpg"

----------

CherryBlog implements a very simple blogging website.

- Posts: the main content of the blog
- Pages: the extra static pages like the 'about'
- Tags: each post has one or multiple tags
- Search: a word(s) based search on the posts and pages
- Caching: in memory caching of data and content
- Drafts: drafts are pages that are not published yet, only visible in development
- URL rerouting: the final URL is not necessarily the path to the file 

CherryBlog is written in Python 3 and uses Jinja2 templating.  The default theme uses Bootstrap.  CherryBlog uses CherryPy as web framework, hence its name.

Content can be written in simple MarkDown !

CherryBlog is open sourced and is licensed under the MIT license.

