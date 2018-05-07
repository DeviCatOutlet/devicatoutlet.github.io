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

  (Notes from Devi)
  1) Left-aligned and Centered
Only adjustment I see at the moment is to align the character descriptions to the left instead of being centered. 
Titles for pages as well as sections within a page can be centered (most of which are already) Only exception
is the "name / title / personality etc" sections for the character pages (these can be left-aligned)

In short:
Titles = centered
Bullet points / descriptions = left-aligned

 2) "A-Channel" is the title of the anime. See here: https://myanimelist.net/anime/9776/A-Channel

 3) Yes, they should receive trailing hearts.

 4) This should be hearts instead of sparkles as well.
 Ideally would prefer:
 Hearts for main headings.
 Sparkles for sub headings (reference Hanabi Character page / art tips)
 Normal bullet points for anything else instead of sparkles.

 EXTRA NOTE:
 Could we swap out the purple heart for this one? 💙