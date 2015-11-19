from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Kitchen Order",
					"description": _("KOT")
				},
				{
					"type": "doctype",
					"name": "Kitchen Receiver",
					"description": _("Receive Kitchen Items.")
				},
				{
					"type": "doctype",
					"name": "Counter Receiver",
					"description": _("Receive Counter Items.")
				},
			]
		},
		
	]