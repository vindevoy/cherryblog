# ABOUT CherryBlog


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


# DOCUMENTATION


## WARNING

**This project is still rather new and is only in version 1.x. Hence the documentation is very short.  It is provided for people who really want to dig into the project.**

## Installation

For now, the only way to install the software is to clone the Git repository: [https://github.com/vindevoy/cherryblog](https://github.com/vindevoy/cherryblog)

### Requirements

Operating system: 

- Linux or Mac OSX.  
- Windows: Sorry, I do not yet support Windows.

Python:

- Python 3 is required.  

Other software:

- Git (optional): to clone the repository. Alternatively you can download the software as a zip.
- Make (optional): to run the basics commands. You can run without make if you type the commands found in the Makefile.

### Downloading libraries

A Makefile is provided.  Run it using make.

```
make dependencies
```

### Running the server

There are 2 methods to run the server at this moment:

- on the localhost for development
- on a production alike environment

You can add environments copying the files to YOUR_ENVIRONMENT.yml in the environments directory (/src/data/environments) and specifying the environment on the command line:

```
python3 ./src/application/serve.py --env YOUR_ENVIRONMENT
```

#### Running development on localhost

By default, you are running on localhost, allowing the most efficient way to debug.

```
make develop
```

#### Running the site 'in production'

Rename the production.sample file into production.yml in the same directory and adapt the settings as needed. If you want to run on port 80, you must run as root (or via sudo). This is unsafe and it's better to use a proxy like Nginx or Apache.

```
make production
```


# CREDITS


Many thanks to everybody who wrote software that I'm using.  Thanks also to the photographers who share their work.

## Language

CherryBlog is written in Python 3: 

- [https://www.python.org/](https://www.python.org/) 

## Python libraries

CherryBlog uses the following Python libraries:

- cherrypy: [https://cherrypy.org/](https://cherrypy.org/)
- markdown: [https://pypi.org/project/Markdown/](https://pypi.org/project/Markdown/)
- pyyaml: [https://pyyaml.org/](https://pyyaml.org/)
- jinja2: [https://pypi.org/project/Jinja2/](https://pypi.org/project/Jinja2/)

# Templating engine

- Jinja2: [https://jinja.palletsprojects.com/en/2.11.x/](https://jinja.palletsprojects.com/en/2.11.x/)

## Bootstrap template

The default template is based on the startbootstrap.com templates downloaded from:

- [https://startbootstrap.com/templates/blog-home/](https://startbootstrap.com/templates/blog-home/)
- [https://startbootstrap.com/templates/blog-post/](https://startbootstrap.com/templates/blog-post/)

## Images

Images downloaded:

- <a href="https://pixabay.com/users/jingoba-24598/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=212601">Jiří Rotrekl</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=212601">Pixabay</a>
- <a href="https://pixabay.com/photos/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=839864">Free-Photos</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=839864">Pixabay</a>
- <a href="https://pixabay.com/users/ulleo-1834854/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3477927">Ulrike Leone</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3477927">Pixabay</a>
- <a href="https://pixabay.com/users/Couleur-1195798/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1437707">Diese lizenzfreien Fotos darfst du zwar verwenden</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1437707">Pixabay</a>
- <a href="https://pixabay.com/users/Hans-2/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=324175">Hans Braxmeier</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=324175">Pixabay</a>
- <a href="https://pixabay.com/users/Hans-2/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1260641">Hans Braxmeier</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1260641">Pixabay</a>
- <a href="https://pixabay.com/users/webandi-1460261/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3308735">Andreas Lischka</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3308735">Pixabay</a>
- <a href="https://pixabay.com/users/gayulo-3585927/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3238564">gayulo</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3238564">Pixabay</a>

SVG downloaded for logo:

- <a href="https://commons.wikimedia.org/wiki/File:Fruit-cherries.svg?uselang=fr">https://commons.wikimedia.org/wiki/File:Fruit-cherries.svg?uselang=fr</a>

## Inspiration

- JBake: [https://jbake.org/](https://jbake.org/)
- Pelican: [https://blog.getpelican.com/](https://blog.getpelican.com/)