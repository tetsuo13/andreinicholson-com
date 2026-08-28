---
date: 2026-08-27
lastmod: 2026-08-27
draft: false
slug: when-to-trigger-sieve-scripts-to-learn-messages-in-dovecot
title: When to Trigger Sieve Scripts to Learn Messages in Dovecot
description: >
  Hint: rarely.
  Sieve scripts can be used as triggers for calling Rspamd.
  Even though it's tempting to trigger them on every message's deletion, you probably shouldn't.
---

This covers a few basic setups for [Dovecot](https://dovecot.org/) that are used to trigger Sieve scripts, specifically for spam/ham learning. For the most part the spam system should be automatically training itself however sometimes a message that's not spam lands in your Junk folder. Moving it out of there should trigger a Sieve script to run a Bash command for the spam system to learn it as ham. That's the type of scenarios that's covered.

While it'll talk about Rspamd as the email message processing system, this can easily be applied to SpamAssassin or other systems.

It will use the [IMAPSieve](https://doc.dovecot.org/latest/core/plugins/imap_sieve.html) plugin so be sure to have this in the Dovecot config somewhere if it isn't already there:

```
protocol imap {
  mail_plugins = $mail_plugins imap_sieve
}
```

Let's start with the most common strategy for when to trigger a Sieve script to learn.

## Ham in Trash, Spam in Junk

This one is by far the simplest and likely out-of-the-box setup for most Dovecot instances. It follows these basic rules:

1. Message moved into Junk: consider spam.
2. Message moved into Trash: consider ham.

You find a spam message in your Inbox so you move it to Junk. That should trigger a Sieve script to learn that message as spam. After you're done with a message, and you delete it, learn it as ham.

The Dovecot config looks something like this:

```
plugin {
  # 1. Message moved into Junk: consider spam
  imapsieve_mailbox1_name = Junk
  imapsieve_mailbox1_causes = COPY APPEND
  imapsieve_mailbox1_before = file:/usr/lib/dovecot/sieve/learn-spam.sieve

  # 2. Message moved into Trash: consider ham
  imapsieve_mailbox2_name = Trash
  imapsieve_mailbox2_causes = COPY APPEND
  imapsieve_mailbox2_before = file:/usr/lib/dovecot/sieve/learn-ham.sieve
}
```

The Sieve scripts referenced are shown below. They do nothing more than pipe the message contents to an external Bash script which in turn calls the spam system to classify the content as indicated.

```sieve {filename="learn-spam.sieve"}
require "copy";
require "vnd.dovecot.pipe";

pipe :copy "learn-spam.sh";
```

```sieve {filename="learn-ham.sieve"}
require "copy";
require "vnd.dovecot.pipe";

pipe :copy "learn-ham.sh";
```

This is fine for the most part, until you discover users are deleting Junk messages... which causes them to go to Trash... which triggers the `learn-ham` Sieve script on spam...

## Revise, Keeping It Simple

You might be asking yourself *"why would anyone delete a message from Junk when it's automatically deleted anyway?"* And that's a valid question, but it's irrelevant. While messages in Junk should be automatically removed after a period of time, manually deleting it shouldn't reclassify the message as ham.

{{<notice info>}}
Very quickly, deleting messages in Junk that are older than 45 days for all users under the ANDREINICHOLSON.COM domain:

```bash
doveadm expunge \
-u *@andreinicholson.com \
mailbox Junk \
BEFORE 45d
```

This uses the [`doveadm`](https://doc.dovecot.org/latest/core/man/doveadm-expunge.1.html) tool. Add it to **dovecot**'s cron (or whatever the `default_internal_user` setting is set to).
{{</notice>}}

It's worth taking a step back to look at the setup as a whole. Rspamd has already processed the message by the time it lands in the mailbox. The [autolearn portion of the statistics config](https://docs.rspamd.com/configuration/statistic/) should be configured to learn when the score is significantly far into the spam or ham threshold while messages that fall somewhere in the middle remain unlearned due to their uncertainty. So not every message is intended to be classified in a binary fashion.

That's a feature. Feeding the message to be learned as ham simply because it was deleted isn't significant.

So reduce the ruleset to its most basic set:

1. Message moved into Junk: consider spam.
2. Message moved from Junk to Inbox: consider ham.

That's it. This only covers the false positive scenario and nothing more.

The Dovecot config:

```
plugin {
  # 1. Message moved into Junk: consider spam
  imapsieve_mailbox1_name = Junk
  imapsieve_mailbox1_causes = COPY APPEND
  imapsieve_mailbox1_before = file:/usr/lib/dovecot/sieve/learn-spam.sieve

  # 2. Message moved from Junk to Inbox: consider ham
  imapsieve_mailbox2_name = INBOX
  imapsieve_mailbox2_from = Junk
  imapsieve_mailbox2_causes = COPY
  imapsieve_mailbox2_before = file:/usr/lib/dovecot/sieve/learn-ham.sieve
}
```

The Sieve scripts don't need to change.

The approach is even promoted on Rspamd's guide how on [how to get feedback from users with IMAPSieve](https://docs.rspamd.com/tutorials/feedback_from_users_with_IMAPSieve/).

