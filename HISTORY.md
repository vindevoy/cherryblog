# Release v1.6.0


- author: Yves Vindevogel (vindevoy)
- date: 2020-05-17

## New Features

- URL rerouting has been implemented on the level of the posts, pages and tags.  This means that you can change the URL of the publication and through the rerouting, it will map the correct document(s).  This can be used to make URLs more readable.
- Support for draft pages has been included.  If you are writing a new post or page, but you don't want it to be published yet, you can put it as draft in the meta data.  You can decide through the environment.yml if you want to show drafts or not (development vs. production).  

## Enhancements

- A sitemap.xml file can be generated from the Makefile.  This allows Google to crawl the website better.
- The application controller class now uses htmlmin to remove all the comment in the HTML, remove double spaces and so on.  This results in a smaller HTML going over the wire, but it also results in a better memory footprint for caching.

## Other

- A Facebook page has been created for marketing reasons.  Why else ?

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/13](https://github.com/vindevoy/cherryblog/milestone/13)


# Release v1.5.2


- author: Yves Vindevogel (vindevoy)
- date: 2020-05-08

## Hotfix

- There was a runtime-error on the posts and pages if they had to tags. This resulted in a TypeError, and in code the KeyError was captured.  

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/15](https://github.com/vindevoy/cherryblog/milestone/15)


# Release v1.5.1


- author: Yves Vindevogel (vindevoy)
- date: 2020-05-07

## Bug Fixes

- There was a problem with the search results. The font weight (bold) of found text in the search results is now case-insensitive.  

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/14](https://github.com/vindevoy/cherryblog/milestone/14)


# Release v1.5.0


- author: Yves Vindevogel (vindevoy)
- date: 2020-05-01

## Features

- Search widget, with minimal number of characters
- Word(s) based search on all the pages and posts
- Case-insensitive search
- Search results with highlight of the word searched
- Number of occurrences of the searched word(s)
- Author and date of each search result
- Image on top of the page is the image of the first result found
- Uses cache for during search, but does not cache itself
- Exclude pages or posts from the search

## Enhancements

- Default settings for items not in the environment files
- Ability to switch of caching (localhost during development)
- Tags are shown on the bottom of the page or post
- Dates are now written in a nicer format
- Better passing on of data through-out the templates
- Commenting in the templates

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/12](https://github.com/vindevoy/cherryblog/milestone/12)


# Release v1.4.2


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-26

## Enhancements

- Added a simple re-route script to re-route HTTP to HTTPS. Can be used if you don't want to run behind an NGINX or Apache.

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/11](https://github.com/vindevoy/cherryblog/milestone/11)


# Release v1.4.1


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-25

## Fixes

- Colour of the background for code is now aligned with the colour of the boxes
- Blue border is gone on the buttons on the home page (primary buttons)
- Margin problem on the tags for smaller screens
- No data showing in the version widget on smaller screens
- External links go in a new tab or window
- Tags now also display page x of y
- MIT License is linked to a Wikipedia page

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/10](https://github.com/vindevoy/cherryblog/milestone/10)


# Release v1.4.0


- author: Yves Vindevogel (vindevoy)
- date: 2020-04-25

## Enhancements

- Added the code to start with HTTPS instead of HTTP
- CherryBlog.org will run on HTTPS from now on

### Github 

For more information on this release, see the issues for this milestone:

- [https://github.com/vindevoy/cherryblog/milestone/9](https://github.com/vindevoy/cherryblog/milestone/9)


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


