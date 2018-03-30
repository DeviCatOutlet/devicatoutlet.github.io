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
* "A-Channel" or "A Channel"? (cf /about) Check proper styling. SPACE EN-DASH SPACE
  seems unlikely, but what is actually correct?
* Character page has hearts on only one side of its headingish lines. Should they
  receive trailing hearts as well, for consistency? Would also mean they can be
  done with the {: .hearts} marker instead of the long-winded image directives.
* Gratitude Board is the only page that has sparkles bracketing a heading. Every
  other page uses hearts. Does it want to use hearts too? Or will sparkles be
  potentially used elsewhere, making it worth having a directive to add them?
