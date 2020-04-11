---

title: "Documentation"

image: "blossom2.jpg"

author: "Yves Vindevogel"
date: "2020-04-08"

----------

## WARNING

**This project is brand new and is only in version 1.x. Consider this release to be an announcement release. Hence the documentation is very short.  It is provided for people who really want to dig into the project.**

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

