background-image: url(images/codecamp-partners.png)
---

class: question

# Eventsourcing 101

## What, Why, and How.

???

I want to talk about event sourcing, what it is, why you might want to do it, and how to actually get started.

---
.definition[
.medium[Bob Gregory]
.light[Application architect at Made.com]
.important[@bob_the_mighty on twitter]
.light[
        Slides and code are available on github
]
]

.footnote[
www.github.com/bobthemighty/eventsourcing-101
]

???

I'm Bob, I'm the application architect at Made.com. You can follow me on Twitter if you like people being angry about politics, and you can find the slides and code sample on github.

---

# What is Eventsourcing?

.definition[
.medium[An architectural pattern]
.light[ where instead of persisting]
.medium[changes to state]
.light[we persist]
.important[a series of events]
]

???


Okay so what *is* eventsourcing?

Blah.


---
class: code-slide

# What is Eventsourcing?
## Instead of this:

```sql
*UPDATE users
   SET name = 'fred'
   WHERE userid = 1234
```
???
What we mean by that is in most applications, like if you're writing Django or Rails or whatever then you have a model where you fethc state from the database
And then you issue an UPDATE statement to go and make changes. If you want to edit a user's name, for example, then you update the users table and you change the name field.
In eventsourcing, we dont' do that. Instead

--
## We do this:

```sql
*INSERT user_events (type, data, entity)
VALUES (
    'user_name_changed',
    'fred',
    1234
)
```

???

we model the domain as a list of events. In order to change the user's name, we insert a new user_name_changed event into our user_events table. We never go back and UPDATE anything, we only ever append new data.

That's it.

---

class: question

# Why?

???

Obvious question: why?

Well there are a bunch of benefits. It can help us when we're trying to figure out how a business process works, and it has some nice benefits for testability, but I'd like you to think about some domains you're already familiar with.
Firstly: when you go to the ATM and see you have 1000 Lei, you take out 100 Lei, why doesn't your bank do this?

---
class: code-slide

## Why don't banks do this?

```sql
UPDATE accounts
  SET balance = 900
   WHERE account_id = 12345
```
???

Why can't banks just update your balance, set it to the new value?

---
class: code-slide

## Because one day they'll do this

```sql
UPDATE accounts
*  SET balance = -42.53
   WHERE account_id = 12345
```

???

Well it's because one day, they'll set it to a value that you don't like, and then you're going to walk into the branch with a mean look on your face and you're going to say

---

class: question
# Dude, where's my money?

???

What happened to all my money? Why am I poor?

And the nice bank clerk will sit you down and get you a coffee, and they'll show you your bank statement.

---

background-image: url(images/bank-statement.png)

???

And they'll say "Well, Mr Gregory, you were paid a load of money at the beginning of the month, but then your wife and children spent it all on trinkets and gew-gaws and knick-knacks and miscellaneous sundries, and now there isn't any left. Now can you please calm down, because you're making a scene."

---
class: definition-slide
## Why do banks store lists of transactions?

.definition[
.medium[Financial reporting]
.light[is modelled as]
.important[a series of events]
]

???

So banks, and accountants, store their data as lists of events. And they do this for a simple reason.

---
class: definition-slide

## Why do banks store lists of transactions?

.definition[
.medium[Financial reporting]
.light[requires us to]
.important[maintain a full history]
]

???

It's important in financial systems that we can keep a full history, and that we can answer questions to auditors.

---
class: definition-slide

## Why do banks store lists of transactions?

.definition[
.medium[Financial reporting]
.light[requires us to]
.important[provide robust auditing]
]

???

If all you know is the current balance, you can't use that to work out how much tax to pay, for example.


---

class: question
# Why is Git so awesome?

???

Okay, why is git so awesome?

The first answer is that we can have a fantastic idea for our code, and then we can stay up until 3 am going hack-hack-hack-hack, and then in the morning, when we're sober...

---

## Git lets us recover from our mistakes

```terminal
bob@localhost ~/code/made/hacienda/ $ git revert HEAD~1

Revert "Lol. Drunk and its 3am. does this wrk yet?"

This reverts commit aa4c03d362246bae32df09764184c3af88f1d412.

# Please enter the commit message for your changes. Lines starting
# with  '#' will be ignored, and an empty message aborts the commit.

# on branch master

# Changes to be committed
#   deleted:    poop.py
#   deleted:    hands.js
#   deleted:    abstractfactorybeanproxymanagerfactoryfactorybuilderconfig.java
```

???

We acn say "Oh, that was actually a terrible idea. Hey, git, that stupid thing I did? Make it so that it never happened, please."

And we just revert the change and pretend it never occurred.

---
class: question

## Git can answer questions

???

But more than that, git can answer questions for us.


---
class: code-slide
## Why does the code look like this?

```terminal
bob@localhost ~/code/made/very-important-project $ git log

*   <span style="color:olive;">56f6a1b7</span><span style="color:olive;"> (</span><span style="color:teal;font-weight:bold;">HEAD -&gt; </span><span style="color:green;font-weight:bold;">master</span><span style="color:olive;">, </span><span style="color:red;font-weight:bold;">origin/master</span><span style="color:olive;">, </span><span style="color:red;font-weight:bold;">origin/HEAD</span><span style="color:olive;">)</span> Merge pull request #624 from madedotcom/latest-events-reader-for-ats
<span style="color:red;">|</span><span style="color:green;">\</span>  
<span style="color:red;">|</span> * <span style="color:olive;">3afdc746</span> simplify a couple more tests using event reader
<span style="color:red;">|</span> * <span style="color:olive;">84f0471b</span> events reader that only returns events from after the test starts
<span style="color:red;">|</span><span style="color:red;">/</span>  
*   <span style="color:olive;">cc2230e9</span> Merge pull request #622 from madedotcom/fix-sftp-motd
<span style="color:olive;">|</span><span style="color:blue;">\</span>  
<span style="color:olive;">|</span> * <span style="color:olive;">0fc716d6</span> I guess SFTP deploy URL is this one
<span style="color:olive;">|</span><span style="color:olive;">/</span>  
* <span style="color:olive;">eb4d9eee</span> BOS-511 Finalise remaining shipments in file if a shipment in a file is already complete (#598)
*   <span style="color:olive;">3a07dad8</span> Merge pull request #619 from madedotcom/readme-stuff
<span style="color:purple;">|</span><span style="color:teal;">\</span>  
<span style="color:purple;">|</span> * <span style="color:olive;">cbb60669</span><span style="color:olive;"> (</span><span style="color:red;font-weight:bold;">origin/readme-stuff</span><span style="color:olive;">)</span> add docs re how to run integration tests
<span style="color:purple;">|</span> * <span style="color:olive;">4ff8672a</span> add info to readme re: how to restart hacienda in containers for acceptance tests
<span style="color:purple;">|</span><span style="color:purple;">/</span>  
* <span style="color:olive;">abb094be</span><span style="color:olive;"> (</span>refs/bisect/bad<span style="color:olive;">)</span> Handle skip message in sqs (#618)
<span style="color:teal;">|</span> * <span style="color:olive;">007cfd8f</span><span style="color:olive;"> (</span><span style="color:red;font-weight:bold;">origin/BOS-185_new</span><span style="color:olive;">)</span> Purchase Orders and Files pages
<span style="color:teal;">|</span> * <span style="color:olive;">ee7fbaf0</span> Order and cancellation file names
<span style="color:teal;">|</span> * <span style="color:olive;">9907bebc</span> Collapse search
<span style="color:teal;">|</span> * <span style="color:olive;">321d544a</span> BOS-185 - navbar and home page with images
<span style="color:teal;">|</span> * <span style="color:olive;">2da34fe2</span> Form search for other fields
<span style="color:teal;">|</span> * <span style="color:olive;">3b5caf13</span> Filtering with SQL query according to order_ref and order_line_ref
<span style="color:teal;">|</span> * <span style="color:olive;">19ff0514</span> BOS-185 - hacienda status UI prototype with orders retrieved from DB
<span style="color:teal;">|</span> <span style="color:red;font-weight:bold;">|</span> * <span style="color:olive;">fd4ed347</span><span style="color:olive;"> (</span><span style="color:red;font-weight:bold;">origin/bos-509-finalisation-manager</span><span style="color:olive;">)</span> BOS-509 WIP Fix broken handlers and add debugging warning logs.
<span style="color:teal;">|</span> <span style="color:red;font-weight:bold;">|</span> * <span style="color:olive;">69d96b4d</span> Fix broken line after rebasing
<span style="color:teal;">|</span> <span style="color:red;font-weight:bold;">|</span> * <span style="color:olive;">a2f47de0</span> start using new finalisation handler to process events. should break things.
```

???

Like "How did we get here?" What were the sequence of decisions that led to this particular design?

---
class: code-slide
## What was I thinking?!
```terminal
bob@localhost /code/made/availability $ git show 2fee

<span style="color:olive;">commit 2fee2846a981d1f42273eb8aae7dc5d74be2054f</span>
Author: Bob Gregory &lt;bob@made.com&gt;
Date:   Mon Dec 19 10:41:39 2016 +0000

    This commit removes events for LeadTimeCap

    Previously, when we created a batch, or changed the ETA of a batch,
    such that the ETA of the batch was > than some configured value, we
    would schedule an event in the future for re-calculating availability.

    This causes an unending stream of errors in the slack channel, and is
    useless given that we recalculate availability daily anyway.
```

???

And we can drill down into one of those decisions and understand the context - why did I delete all that code? What was I trying to achieve at that time?

---
class: question

# Git can even rewind time

???

But git can do more than that. It can rewind time...

---
class: code-slide

## ... And play it forward to get a different result

```terminal
bob@localhost ~/code/made/very-important-project $ git rebase HEAD~10

pick   508bea9 Replacing orders stream with ce-order
squash 7ba9da9 Updated order_placed event reader to handle non-uk orders. lulz
fixup  f63c701 Update to latest atomicpuppy
fixup  664d934 Change ES url in jenkinsfile for test (#140)
reword 1d04849 Adding operators.md for egidijus (#141)
fixup  5a365c3 more truth in the readme
pick   7e69788 Added nomad security group to redis security group (#142)
reword 1c2b1d2 maybe when event consumer runs, evenstore is not running, so the acceptance tests fail, lets make eventstore a dependancy for eventconsumer
squash 0ebdd5a maybe we will see what is running and what is not, because eventstore is allegedly down.
pick   c6d376e Removed metrics, replaced with Striemann; made Jenkinsfile use make (#143)

# Rebase ca177fb..c6d376e onto ca177fb (10 commands)
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out

```

??? 

And then play it forward again in a new way. Git rebase is a hugely powerful command because it lets me skip and re-order and even *edit* decisions I made in the past, to create a new current state from the historical record.


---
class: definition-slide
## What makes git useful?

.definition[
.medium[Git stores a rich history]
.light[modelled as a]
.important[series of events]
]

???

So why is git so useful? Because it stores a list of events about what we did.

---
class: definition-slide
## What makes git useful?

.definition[
.medium[Git allows us to rewind time]
.light[and interrogate the events by]
.important[capturing our intent]
]

???

And because we can rewind and ask questions about those events, because they capture our intent. The commit messages tell us what we were trying to DO when we made that change, and so we can understand the full context of a decision.

---
class: question
# Git __applies__ events to build a working tree.

???

This is an important idea, and one that we'll return to shortly - when we're working with git, we don't interact with the commits directly very often. For the most part, we're just looking at files. Git applies all the events to an empty working tree to produce the files in our code base.

---
class: question

# So What?

???

Okay, so you might be thinking "I don't write source control systems, or banking applications. The last thing I wrote was an iphone app for booking meeting rooms. I mostly build e-commerce shops in Wordpress. What has this got to do with me?"

Well I want you to think about a scenario. Imagine that you're at your desk with your headphones on and you're going hack-hack-hack when your boss walks up, and he's like "Oh, hey Bob!" which is weird, because your name isn't Bob, but he's your boss, so whatever, and he says "Bob, we're going to build an e-commerce site, to sell rocks and socks and clocks and blocks in a box and I want *you* to write the shopping cart."

---

class: definition-slide

# Requirement
.definition[
.medium[As a user]
.light[I need to be able to]
.important[add items to my shopping basket.]
]

???

And you're like "YES!" because you _love_ writing shopping carts. Every time you learn a new language, the first things your write are Hello World, a to-do list application, and a shopping cart, so you've got this down. You put your headphones back on and go hack-hack-hack and twenty minutes later...

---

class: code-slide

# Solution!

## Store a json blob in Mongo. Go home early.

```python
def insert(items):
    return db.baskets.insert_one(items).inserted_id

def update(basket_id, items):
    result = db.baskets.update(
        {"_id": ObjectId(basket_id)},
        items
    )
    return items['_id']

def get(basket_id):
    data = db.baskets.find_one(ObjectId(basket_id))
    del data['_id']
    return Counter(data)
```

???

You have a working shopping cart. It stores data as json blobs in mongo db, because mongo is awesome, and you go home. The e-commerce site is a huge success and your boss is very happy, and you get a promotion, and everything is amazing, until a year later when your boss comes over to your desk and he says, "Bob - we have a problem", and you think, "How can there be a problem? I used mongo and everything" but he says, "Nobody is buying our clocks any more."

He shakes his head sadly and says "We don't know why, but we have two guesses. Recently we changed our product page, and the marketing team think maybe the usability has suffered, so maybe people aren't adding clocks to their carts any more, but we also changed our shipping prices, and the UX designer thinks maybe it just costs too much to ship clocks.


---

class: requirements

# Requirement
.medium[We need to know which of these is true:]
1. .light[Users aren't adding clocks to their baskets.]
2. .light[Users are removing clocks at the checkout.]

???

So we need to know, Bob, are people just not adding clocks any more, or do they remove them at checkout? Can you help?

And he looks down at you, and you look back at him, deep into his eyes and you say...


---

class: question

# Dude, all I have is this json blob.

???

Dude, like I literally have no idea. What am I, psychic?


---

class: fullscreen-image
background-image: url(images/basket-event-streams.svg)

# Why can't our json blob help?


???

Because our json blob is useless here. It can't answer this question. But why?

Well, here we have two scenarios. In the first, we add rocks and clocks to our basket, but we remove the clocks at checkout. In the second, we only add rocks in the first place. Looking at the final state, we can't tell the two apart.

---
class: definition-slide
# Why can't our json blob help?
.definition[
.medium[Our simple mongo basket]
.light[only captures the current state]
]

???

Our json mongo basket only stores the current state. Every time we add a new item, we overwrite all the previous data.

---
class: definition-slide
# Why can't our json blob help?
.definition[
.medium[Our simple mongo basket]
.light[only captures the current state]
.important[so it _loses_ valuable data]
]

???

And that means that we lose that data. We didn't know it was important to know when someone removes a clock, but it is.

---
class: definition-slide
# Why can't our json blob help?
.definition[
.medium[Our simple mongo basket]
.light[only captures the current state]
.important[so it _loses_ valuable data]
.important[and can't capture the user's _intent_]
]


???

And because we lose the data, we lose the user's intent. We can't look at the commit log and ask "How did we get here? What was the user thinking?"

---

class: question

# Eventsourcing is like Git for our domains.

???

So eventsourcing is like git for our data. It lets us rewind time and ask questions.

---

class: code-slide

# Anyone else ever do this in prod?

```sql
UPDATE users
    SET email = 'bob@made.com'
    WHERE userid = 98765
```

???

Have you ever gone into production to make a quick change?

---

class: code-slide

# But actually end up doing this?

```sql
UPDATE users
    SET email = 'bob@made.com'
```

???

And forgotten a where clause? You realise, just after you start the query running that you've done a Terrible Thing, and then you pull this face

---

class: fullscreen-image
background-image: url(images/get-out.jpg)


???

This happened to me.

---
class: definition-slide

.definition[
.light[What if we could]
.medium[revert our mistakes?]
]

???

What if we could just revert that? If we could say "Hey, that stupid thing I just did? Make it so it never happened".

---
class: definition-slide

.definition[
.light[What if we could]
.medium[rewind time to reproduce bugs?]
]

???

What if we could rewind time. You ever have a bug that you couldn't reproduce? What if you could checkout your production system to a point in time and then play it forward again to see what happened in slow-motion?

---
class: definition-slide

.definition[
.light[What if we could]
.medium[replay time to make reports?]
]

???

What if we could replay time in a different order, or with a different view function to produce any report we could think of?
When our boss comes to our desk and calls us Bob, we can just go write a function that reports how many people have removed clocks this week, and last week, and *Any* week in the history of our site.

---

class: question

# How?

???

So now your minds are blown, let's talk about how to actually do this. First I need to cover some quick definitions.

---
.definition[
.medium[Command:]
.light[a request to the system]
.important[to _do_ something]
]

???

A command is a request to the system. When I say "Stand up" that's a command.

---
.definition[
.medium[Command:]
.light[uses __imperative__ tense:]
* Add Item To Basket
* Select Shipping Option
* Launch Nuclear Missiles
]

???

When naming commands we use the imperative tense. So Add Item to Basket, or Launch Nuke is a command. It doenst' matter where the request comes from. It could be an API call, or a button push, or from reading a CSV file.

---
.definition[
.medium[Event:]
.light[a record that the system]
.important[_did_ something]
]

???

An event is a record that we *did* a thing already.

---
.definition[
.medium[Event:]
.light[uses __past__ tense:]
* Item Added to Basket
* Shipping Option Selected
* Nuclear Missiles Launched
]

???

We use the past tense to name them, so Item Added to Basket, or Nuclear Missile Launched is an event name. Events, in eventsourcing, are the result from invoking a command.

---
class: code-slide
# Events are immutable objects

```python
from typing import NamedTuple

class UserRenamed(NamedTuple):
    user_id: int
    name: str
```

???

We usually represent events as immutable objects. Events have no behaviour, they're just data. Here's an event in Python.

---
class: code-slide
# Events are immutable objects

```haskell
data UserNameChanged = UserNameChanged {
     userId :: Int
   , name :: String
}
```

```fsharp
type UserNameChanged = { UserID: int; name: string }
```

???

And here's how I might do it in Haskell and F#

---
class: code-slide
# Events are immutable objects

```csharp
public class UserNameChanged 
{
    public int UserId { get; }
    public string Name { get; }

    public UserNameChanged(int userId, string name) 
    {
        UserId = userId;
        Name = name;
    }
}
```

???

And here's the same event in C#.


---
class: question
## It's okay to refuse a command

???

When processing a command, we can say "no". Like if I say "Stand up", you can say "No way, man, I'm just watching this talk. Stop doing that, it's weird".

---
class: question
# Once an event has happened

???

But if an event has happened, then it's _happened_.

---
class:fullscreen-image
background-image: url(images/Castle_Bravo_Blast.jpg)
## It _stays_ happened

???

If the event says Nuclear Missile Launched, it's no good closing your eyes and saying "No it didn't."

---
.definition[
.medium[Aggregate:]
.important[an eventsourced entity]
.light[don't worry too much about this]
]

???

Okay, last definition. An aggregate is an entity that manages other entities. It's a term from DDD, we don't need to talk about that too much right now, but this...

---
class: code-slide
```python
class Aggregate:
    """
    Base class for event sourced aggregates
    """
*    def __init__(self, events=None):
        self.events = events or []
        self.new_events = []
        self.replay()

    def replay(self):
        for e in self.events:
            self.apply(e)

    def apply(self, e):
        # find a "handler" function
        # call the function with the event
        pass

    def write_event(self, e):
        self.events.append(e)
        self.new_events.append(e)
        self.apply(e)
```

???

This is a base class for an aggregate. Notice that it has a constructor that takes a list of events. When I load this aggregate from my eventstore - the database - I'll give it all the events I saved, and it will replay them.

---
class: code-slide

```python
class Aggregate:
    """
    Base class for event sourced aggregates
    """
    def __init__(self, events=None):
        self.events = events or []
        self.new_events = []
        self.replay()

*    def replay(self):
        for e in self.events:
            self.apply(e)

    def apply(self, e):
        # find a "handler" function
        # call the function with the event
        pass

    def write_event(self, e):
        self.events.append(e)
        self.new_events.append(e)
        self.apply(e)
```

???

Replay just says "For every event in my history, apply the event".

---
class: code-slide

```python
class Aggregate:
    """
    Base class for event sourced aggregates
    """
    def __init__(self, events=None):
        self.events = events or []
        self.new_events = []
        self.replay()

    def replay(self):
        for e in self.events:
            self.apply(e)

*    def apply(self, e):
        # find a "handler" function
        # call the function with the event
        pass

    def write_event(self, e):
        self.events.append(e)
        self.new_events.append(e)
        self.apply(e)
```

???

And apply just updates my state somehow. Remember that we're not saving our state in teh database, so we need to rebuild it each time from the events.

---
class: code-slide

```python
class Aggregate:
    """
    Base class for event sourced aggregates
    """
    def __init__(self, events=None):
        self.events = events or []
        self.new_events = []
        self.replay()

    def replay(self):
        for e in self.events:
            self.apply(e)

    def apply(self, e):
        # find a "handler" function
        # call the function with the event
        pass

*    def write_event(self, e):
        self.events.append(e)
        self.new_events.append(e)
        self.apply(e)
```

???

Lastly there's a write_event method that adds a new event into our history. We store it in the "new_events" collection and apply it. The reason for the new_events collection is that when we come to save this aggregate, we're just going to insert those new events. Remember that we never go back and update our events, only insert new ones, so separating them here makes it easy to know what's changed.

---
class: fullscreen-image
background-image: url(images/eventsourcing-cycle.svg)

???

This is the most important slide. I stole this description from Jeremie Chassaing. You should watch his talks, he's smarter than I am, and more handsome, and French. When we're implementing eventsourcing, this is how it works. A request comes into the system - a command - we look at our current state to decide what to do, and when we've decided, we create a new event to record that decision.

Lastly, we apply that event to our state to update it.

---
class: code-slide
# An example
.light[(not production ready)]

```python
class MissileSilo(Aggregate):

    def launch_missile(self, secret_code):
        """
        Decide whether to launch and record the decision
        """

*       if secret_code != "999":
           raise ValueError("That's not the code, the code is 999")

        if not self.is_launchable(missile_id):
           raise UnlaunchableMissile(missile_id)

        self.__send_launch_signal(missile_id)

        self.write_event(MissileLaunched(missile_id))


    def on_missile_launched(self, event):
        """
        Apply the event
        """
        self.missiles.pop(event.missile_id)
```

???

Here's an example. We have a missile silo class, that is an aggregate. There's a command "Launch Missile". When we handle that command the first thing we do is decide whether the secret code is valid.

---
class: code-slide
# An example
.light[(not production ready)]

```python
class MissileSilo(Aggregate):

    def launch_missile(self, secret_code):
        """
        Decide whether to launch and record the decision
        """

        if secret_code != "999":
           raise ValueError("That's not the code, the code is 999")

*       if not self.is_launchable(missile_id):
           raise UnlaunchableMissile(missile_id)

        self.__send_launch_signal(missile_id)

        self.write_event(MissileLaunched(missile_id))


    def on_missile_launched(self, event):
        """
        Apply the event
        """
        self.missiles.pop(event.missile_id)
```

???

If the code is valid, we need to decide if we have enough missiles to launch one. Assuming we do, we're going to send the signal to start the countdown.

---
class: code-slide
# An example
.light[(not production ready)]

```python
class MissileSilo(Aggregate):

    def launch_missile(self, secret_code):
        """
        Decide whether to launch and record the decision
        """

        if secret_code != "999":
           raise ValueError("That's not the code, the code is 999")

        if not self.is_launchable(missile_id):
           raise UnlaunchableMissile(missile_id)

        self.__send_launch_signal(missile_id)

*       self.write_event(MissileLaunched(missile_id))


    def on_missile_launched(self, event):
        """
        Apply the event
        """
        self.missiles.pop(event.missile_id)
```

???

And, lastly, we reord an event to say what we did.

---
class: code-slide
# An example
.light[(not production ready)]

```python
class MissileSilo(Aggregate):

    def launch_missile(self, secret_code):
        """
        Decide whether to launch and record the decision
        """

        if secret_code != "999":
           raise ValueError("That's not the code, the code is 999")

        if not self.is_launchable(missile_id):
           raise UnlaunchableMissile(missile_id)

        self.__send_launch_signal(missile_id)

        self.write_event(MissileLaunched(missile_id))


    def on_missile_launched(self, event):
        """
        Apply the event
        """
*       self.missiles.pop(event.missile_id)
```

???

Then we have a separate method that *Applies* that event to remove that missile from the list of launchable missiles. It's really really important that we send the launch signal in our decide method, and not in our applies method, because otherwise, every time we load the silo from teh database we're going to send the signal again, and that's going to make it really hard to agree a peace treaty.

---
class: question

Let's write some code

???

So what I'm going to do now is try to write an eventsourced shopping cart, including the datbase stuff, in the next 25 minutes. Obviously it's really hard coding in front of people, and there's a lof of you, so If I actually manage to pull this off, you guys have to give me a massive round of applause. You need to go *absolutely* crazy, okay? Deal.

EXPLAIN THE PANES!
REMEMBER TO BREATHE!

---
class: fullscreen-image
background-image: url(images/codecamp-feedback.png)
