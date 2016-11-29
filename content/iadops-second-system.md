Title: iAdOps and Second-System Effect
Date: 2016-11-29 10:15:02
lat: 41.889365
long: -87.632197

Some of you have already heard my story about the doomed Campaign Management System project (or, more accurately, series of failed projects) back at Leapfrog Online. (Mark will be able to recall his own direct memories.) Of course, LFO already _had_ a Campaign Management System in the form of a custom application built in-house, but there was general agreement that the company's business operations and policies had outgrown the assumptions made in the original design. A project to rethink, redesign, and build an entirely new application was a high priority for Tech from before the first day I got there—and despite any number of project reboots, changes in frameworks, and reconstitutions of the team membership, I was there for more than seven years and never saw anything shipped.

In short, it was a classic case of [the Second-System Effect](http://wiki.c2.com/?SecondSystemEffect) as described by Fred Brooks in the fifth essay of _The Mythical Man-Month_. In particular, the requirement that the new system should do everything that the existing one did, while somehow being "better" in a vaguely defined but comprehensive way, was really impossible to reconcile.

From the c2 wiki:

> If your project is the second system for most of your designers, then it will probably fail outright. If it doesn't fail, it will be bloated, inefficient, and icky.

I am writing this because I have concerns that our current effort to redefine the product design of iAdOps is smelling a lot to me like the restarts of the CMS project that I experienced. The worrying parallels include:

- We judged an incomplete prototype to be on the wrong track without any actual user testing.
- Executive Management repeated the request that any new iAdOps must include all functionality of the existing tool before it can serve as a replacement.
- The decision to reconsider the fundamentals of our previous working design has (so far) produced more uncertainty about, rather than clearer definition of, the project's goals.

I do not mean to say that entirely disagree with reconsidering the product design and approach, only that the dangers of Second-System Effect are lurking nearby, and I wanted to caution everybody to be on guard against the risks. Complete rewrites of existing software fail more often than they succeed. That we have already been working on this for two years and have returned to product design without shipping any working software suggests that we have already succumbed to the effect to some extent

So that I not focus entirely on the problem, here are suggested risk-mitigation strategies:

- Consider whether we can refactor, rather than rewrite, the existing code base.
- Keep goals and scope clear and focused, or make them so.
- Focus on improving, enhancing, or adding one feature at time; we don't have to replace the existing tool all at once.
- Concentrate on specific features, not the general purpose of the application. We can implement features directly, but cannot build abstract ideas as such.
- Apply [YAGNI](http://wiki.c2.com/?YouArentGonnaNeedIt) liberally.
