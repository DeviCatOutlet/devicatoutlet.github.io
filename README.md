# DeviCat

Source code for the [DeviCat Outlet](http://devicatoutlet.com/) web site.

To build and test locally:

* Install Ruby
* gem install bundler
* bundle install
* bundle exec jekyll serve

It should auto-detect changes to Markdown or layout files. If you change the
configuration in _config.yml, restart Jekyll.

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
* No other heading levels are currently used.

### TODO

* Settle what should be left-aligned and what should be centered. Figure out some
  simple rules, and encode those into the CSS, rather than messing with tons of
  specific directives.

  (Notes from Devi)
  1) Left-aligned and Centered
Only adjustment I see at the moment is to align the character descriptions to the left instead of being centered. 
Titles for pages as well as sections within a page can be centered (most of which are already) Only exception
is the "name / title / personality etc" sections for the character pages (these can be left-aligned)

In short:
Titles = centered
Bullet points / descriptions = left-aligned
