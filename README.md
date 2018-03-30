# DeviCat

Source code for the [DeviCat Outlet](http://devicatoutlet.com/) web site.

To build and test locally:

* Install Ruby
* gem install bundler
* bundle install
* bundle exec jekyll serve

It should auto-detect changes to Markdown or layout files. If you change the
configuration in _config.yml, restart Jekyll.

### TODO

* Settle what should be left-aligned and what should be centered. Figure out some
  simple rules, and encode those into the CSS, rather than messing with tons of
  specific directives.
