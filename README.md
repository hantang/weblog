# weblog
A python static blog generator.

## Overview

`Weblog` is a simple static blog generator built with python.

Inspired by [Hugo](https://github.com/gohugoio/hugo/), [Maverick](https://github.com/AlanDecode/Maverick) and [pelican](https://github.com/getpelican/pelican) etc.

mainly techs:
* markdown parser: [mistune](https://github.com/lepture/mistune)
* math support: [ketax](https://github.com/KaTeX/KaTeX)
* date and time parsing: [pendulum](https://pendulum.eustace.io/)
* toml/yaml
* ...

## Demo

Here is: [https://hantang.github.io/weblog/](https://hantang.github.io/weblog/)

Snapshots:
* ![HomePage](images/home.jpg "Home Page")
* ![DarkMode](images/dark.jpg "Dark Mode")
* ![Menus](images/menu.jpg "Menus")
* ![Post](images/post.jpg "Post Example")

## Usage

A example is here:
```shell
# create site dir
mkdir blog-site
cd blog-site

# add posts and write something
mkdir content
touch content/index.md

touch content/about.md
mkdir content/posts
touch content/posts/first-post.md
touch content/posts/new-post.md
mkdir content/projects
touch content/projects/demo.md

# add content
echo -e "# Hi\n\nThis is ..." > content/index.md
echo -e "# About\n\n..." > content/about.md

cat << EOF > content/posts/first-post.md
---
title: "My First Post"
author:
date: "$(date "+%Y-%m-%d %H:%M:%S")"
draft: false
summary: "Write summary here."
comment: ""
---

## Part1

something here...

## Part2

more words...
EOF

# copy config and update
cp ../config/config.toml .

# build markdown to html
python ../runblog.py

# local server
python -m http.server -d deploy

# open `http://localhost:8000`
```

## Themes
### theme-vanilla

* style: mainly from [riggraz/no-style-please](https://github.com/riggraz/no-style-please/)
* fonts: `Megrim` - [John MacFarlane](https://www.johnmacfarlane.net/)
* code highlight: [numist/highlight-css](https://github.com/numist/highlight-css/)
* favicon: created by [favicon](https://favicon.io/) with symbol emptyset `∅`.
