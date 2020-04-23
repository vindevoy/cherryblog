---

title: "Release notes"

image: "blossom4.jpg"

author: "Yves Vindevogel"
date: "2020-04-23"

----------

# Release v1.3.0


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-23

## Enhancements

- Page caching added, next to the data caching (which remains in place for common data)
- Caching is in a class now

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/8](https://github.com/vindevoy/cherryblog/milestone/8)


# Release v1.2.0


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-17

## Enhancements

- Code is now following the Model-View-Controller pattern
- Logging updated for CherryPy and added for CherryBlog
- Updated the caching system, all data is stored in memory
- Server can now run in daemon mode, including user privileges
- Try Except added when reading configuration and content
- Texts are now in I8N directory, for future translations
- Static directories and static files can be served
- Separator is now a setting
- Minor bug fixes


### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/6](https://github.com/vindevoy/cherryblog/milestone/6)


# Release v1.1.1


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-11

## Fixes

- Missing top image in the posts archive
- Alignment of the footer for small devices
- Code boxes were not showing nicely

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/7](https://github.com/vindevoy/cherryblog/milestone/7)


# Release v1.1.0


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-11

## Features

- Introduction on top of the index page
- Footer menu
- Important news widget
- Version widget 

## Theme enhancements

- Categories are now named tags
- H-elements have a slightly different colour now in order to make the text more readable
- Logo added to the top menu and as favicon.ico
- The first post for a tag contributes the image to the top of the page

## Code enhancements

- Logging is now saved
- Root of the theme and data directory can be parameterized
- Makefile enhancements
- Directory updates

## Fixes

- Blog title is bigger, together with the main menu

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/3](https://github.com/vindevoy/cherryblog/milestone/3)


# Release v1.0.2


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-08

## Fixes

- The layout has changed:
    - Menu back to normal size of the original template
    - Code is better highlighted, but not yet fantastic
- Number of types of posts is no longer hard coded.
- Renamed the directory site to settings because it makes more sense.

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/5](https://github.com/vindevoy/cherryblog/milestone/5)


# Release v1.0.1


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-08

## Fixes

- The layout has changed a bit:
    - Less spacing
    - Smaller font
    - Top menu now colours correctly the active menu   
    - History menu item
- A major bug with for instance Facebook was fixed.  No longer is adding things on the URL causing the app to crash.
- Links in the uploaded pages yesterday are working.

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/4](https://github.com/vindevoy/cherryblog/milestone/4)


# Release v1.0.0


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-07

## New features

Highlights:

- Index page with 3 types of posts: 
    - Spotlight post (1 on top)
    - Highlighted posts (2 below)
    - Standard posts (rest)
- Archive of older posts
- Static pages like 'about', 'documentation' and 'credits'
- Categories widget
- Bootstrap tested on smaller devices
    
Base architecture:

- Written entirely in Python 3
- Theming with Jinja 2 
- Bootstrap template 
- Content written in Markdown
- Settings in YAML
- Multi-environment using YAML

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/1](https://github.com/vindevoy/cherryblog/milestone/1)



