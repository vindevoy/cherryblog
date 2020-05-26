---

title: "About CherryBlog"

image: "blossom1.jpg"

author: "Yves Vindevogel"
date: "2020-04-08"
last_update: "2020-05-01"

----------

## Introduction

CherryBlog implements a very simple blogging website.

- Posts: the main content of the blog
- Pages: the extra static pages like the 'about'
- Tags: each post has one or multiple tags
- Search: word based search in posts and pages
- Caching: in memory caching of data and content
- Drafts: drafts are pages that are not published yet, only visible in development
- URL rerouting: the final URL is not necessarily the path to the file 

At this moment, it has the basic news of the project where each article is a post about the new version that was released.

### Goals

As a developer, I want to share things with the world and run a blog. Finding the right blogging software is difficult if you limit the choices for the final deployment.

- (Semi-)static website that can be hosted anywhere behind an Apache or Nginx server. Or even in a S3 bucket for that matter.
- No database to hold the content _(see note)_.  Data must come from local files only.
- Easy to write content in for instance MarkDown.
- Extensible with themes, features, ...

_Note: No database if the site is very small. If there would be a need for a higher performance on features like searching, it can be included._

#### Inspiration

I started using JBake quite some time ago, but the project does not seem very lively.  I ran two sites with it and I was very pleased with it.   

Furthermore, I have switched from the Java (-alikes) world to Python.  In Python, the only thing I tried was Pelican.  Pelican however was not what I needed for another website (my personal site as freelancer) and I found CherryPy as framework.  I was able to make my personal site in just a matter of hours (the content and template was already available from JBake).  When using CherryPy, I saw a possibility to write something similar like JBake in Python.  

For now, I will not create a static website (like JBake and Pelican do), but I will run a website with data coming from Markdown files, YAML files, ...  In a later phase, I want to build the site to a fully static website, with a backend for the dynamic data like comments on posts.  

## Architecture

### Python 

The project is written in Python 3 and uses the CherryPy framework as backend. Hence the name of the project: CherryBlog.  

Python libraries included:

- cherrypy
- jinja2
- pyyaml
- markdown

### Content
The content of the blog is written in MarkDown. On top of each content file, there's a meta data section containing:

- author
- date written
- image on top of the page
- summary of the content
- tags

The whole content is served from local files, so no need for a database like for instance WordPress, Drupal or Joomla.

### Settings

The settings (or configuration) are done in YAML files.  Multiple environments can be used for development and production sites, each with their own settings.

### Theme 

The default theme is based on two themes found on https://startbootstrap.com/templates/

- [https://startbootstrap.com/templates/blog-post/](https://startbootstrap.com/templates/blog-post/)
- [https://startbootstrap.com/templates/blog-home/](https://startbootstrap.com/templates/blog-home/)

The theme is implemented in Jinja2 templates.

## Open source

### License

The project is open sourced under the MIT license and the sources can be found on Github:   

[https://github.com/vindevoy/cherryblog](https://github.com/vindevoy/cherryblog)

At this moment, I (vindevoy) am the only contributor.  I started the project just end of March 2020.

### Version(s)

The current version is depicted in the version widget.  The code is tagged on Github for each released version.

### Roadmap

A set of issues have been logged in Github.  They are all in backlog for now as this is a non-funded project.  The updates are scheduled:

- new releases: each 2 weeks (will update version to x.Y+1.0)
- bug fixes: 2 days after the release (will update version x.y.Z+1)

Each "sprint", a number of issues will be moved from the backend to the new release.

The major release number will be bumped when a major new feature is introduced.  For instance:

- Implementation of the the mongodb backend
- Static site generation

