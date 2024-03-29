# DeviCat

Source code for [DeviCat's](https://devicat.art/) web site.

To build and test locally:

* Install Ruby
* gem install bundler
* bundle install
* bundle exec jekyll serve

It should auto-detect changes to Markdown or layout files. If you change the
configuration in _config.yml, restart Jekyll.

To make the site available on the LAN, add your local IP: `-H 192.168.0.123`

To customize a group of pages, add front-matter to the pages thus:
    ---
    category: foo
    ---
The body tag will then have class="foo-cat" and its contents can be styled
accordingly. All pages which lack this directive will have class="devi-cat" :)

Heading usage:

* H1 ("# Foo") is used once only, at the start of the page. If there are multiple
  lines with this heading style, subsequent ones are displayed smaller.
* H2 ("## Bar") marks the start of a broad section, and will be bracketed with
  hearts.
* H3 ("### Spam") introduces a subsection, and is bracketed with sparkles.
* H4 ("#### Blargh") is used to subdivide lines of images.
* No other heading levels are currently used.

TODO:
* Ensure that everything is (remains) HTML5 and CSS3 standards compliant.
  - https://validator.w3.org/nu/?doc=http%3A%2F%2Fdevicat.art%2F
* Get everything to work (or at least mostly-work) on mobile.
  - Biggest issues are now solved.
  - TODO: Get someone with a phone to try the site and give feedback.
  - Notably, what do touch gestures do? Are they sane? Check the nav.
* A11y compliance:
  - Jumping from H1 to H3 is not recommended. Would be a pain to fix perfectly though.
