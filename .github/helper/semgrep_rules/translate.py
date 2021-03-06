# Examples taken from https://vmraidframework.com/docs/user/en/translations
# This file is used for testing the tests.

from vmraid import _

full_name = "Jon Doe"
# ok: vmraid-translation-python-formatting
_('Welcome {0}, get started with ERPAdda in just a few clicks.').format(full_name)

# ruleid: vmraid-translation-python-formatting
_('Welcome %s, get started with ERPAdda in just a few clicks.' % full_name)
# ruleid: vmraid-translation-python-formatting
_('Welcome %(name)s, get started with ERPAdda in just a few clicks.' % {'name': full_name})

# ruleid: vmraid-translation-python-formatting
_('Welcome {0}, get started with ERPAdda in just a few clicks.'.format(full_name))


subscribers = ["Jon", "Doe"]
# ok: vmraid-translation-python-formatting
_('You have {0} subscribers in your mailing list.').format(len(subscribers))

# ruleid: vmraid-translation-python-splitting
_('You have') + len(subscribers) + _('subscribers in your mailing list.')

# ruleid: vmraid-translation-python-splitting
_('You have {0} subscribers \
    in your mailing list').format(len(subscribers))

# ok: vmraid-translation-python-splitting
_('You have {0} subscribers') \
    + 'in your mailing list'

# ruleid: vmraid-translation-trailing-spaces
msg = _(" You have {0} pending invoice ")
# ruleid: vmraid-translation-trailing-spaces
msg = _("You have {0} pending invoice ")
# ruleid: vmraid-translation-trailing-spaces
msg = _(" You have {0} pending invoice")

# ok: vmraid-translation-trailing-spaces
msg = ' ' + _("You have {0} pending invoices") + ' '

# ruleid: vmraid-translation-python-formatting
_(f"can not format like this - {subscribers}")
# ruleid: vmraid-translation-python-splitting
_(f"what" + f"this is also not cool")


# ruleid: vmraid-translation-empty-string
_("")
# ruleid: vmraid-translation-empty-string
_('')
