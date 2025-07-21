#import "@preview/slydst:0.1.4": *


#show: slides.with(
  title: "Print on Demand",
  subtitle: "PDF Generation for Django",
  authors: "Jonathan Moss",
)

#set text(font: "Barlow")
#show link: underline

#show raw: set block(fill: silver.lighten(65%), width: 100%, inset: 1em)



= The Problem

== Printable Content
#v(8em)
#align(center)[
  HTML is great for the web, for re-flowable content, but not so much for printing
  #v(2em)
  We need to produce PDFs for repeatable and accurate printing 
]

= The Solution

== Ye Olde Times
#v(3em)
Web developers loved to use HTML and CSS. It is what we know... 
We also know that Chrome and related browsers can print directly to PDF.

So the first solution many reach for is to use a headless browser to render regular pages to PDF.

#v(2em)
Print friendly CSS is a thing, and this approach does work, but...

- Installing a headless browser is a pain with lots of dependencies
- It is slow, and requires a lot of resources
- Provides limited control over the outputs print characteristics

#emoji.face.cry #emoji.face.cry #emoji.face.cry

== Weasy Print

Weasy Print is a visual rendering engine for HTML and CSS that can output to PDF.
#v(3em)
- Does *NOT* depend on a full rendering engine like WebKit or Gecko
- Super simple to just `pip install`
- Pure python layout engine
- Supports modern CSS features like flexbox, grid, counters, and more
#v(3em)
Given it take HTML and CSS as input, it can be used to render any HTML content, including Django templates...

= Weasy Print Show & Tell #emoji.face.beam

== Typst

A markup-based typesetting system that is designed to be as powerful as LaTeX while being much easier to learn and use. Typst has:

#v(1em)
- Built-in markup for the most common formatting tasks
- Flexible functions for everything else
- A tightly integrated scripting system
- Fast compile times thanks to incremental compilation
- Friendly error messages in case something goes wrong
- A mechanism for passing in data
- Binding for Rust, Python, Ruby and Typescript...


== Typst & Django

#align(center)[
  #image("a19adk.jpg", height: 15em)
]

wait... that sounds a lot like a templating engine to me.

So lets make it one for Django #emoji.face.nerd

= Typst Engine Demo Time #emoji.face.cool

== Resources

- https://www.github.com/a-musing-moose/pod
  - (hopefully) working code that backs up this talk

#line(length: 80%)

- https://weasyprint.org/
  - The Weasy Print project

- https://github.com/Kozea/WeasyPrint/
  - The Weasy Print Repository

#line(length: 80%)

- https://typst.app/
  - The commercial offering from the Typst team

- https://github.com/typst/typst
  - The open source code for the Typst engine
