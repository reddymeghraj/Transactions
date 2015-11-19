# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		"Transactions": {
			"color": "yellow",
			"icon": "icon-book",
			"type": "module",
			"label": _("Transactions")
		}
	}
