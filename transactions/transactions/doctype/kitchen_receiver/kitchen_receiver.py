# -*- coding: utf-8 -*-
# Copyright (c) 2015, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class KitchenReceiver(Document):
	def on_submit(self):
		date=self.date
		ls=self.kitchen_receiver_item
		for i in range(len(ls)):
			item_name=ls[i].item_name
			item_code=ls[i].item_code
			qnty=ls[i].quantity
			#-------Godown Stock Updation-----------------
			q1=frappe.db.sql("""select quantity from `tabGodown Stock` where item_name=%s and item_code=%s """,(item_name,item_code))
			if q1:
				query=frappe.db.sql("""update `tabGodown Stock` 
				set quantity=quantity-%s 
				where item_name=%s and item_code=%s""",(qnty,item_name,item_code))
				frappe.msgprint("Godown Stock Updated")
			#-------Kitchen Stock Updation-----------------
			q4=frappe.db.sql("""select quantity from `tabKitchen Stock` where item_name=%s and item_code=%s """,(item_name,item_code))
			if q4:
				query=frappe.db.sql("""update `tabKitchen Stock` 
				set quantity=quantity+%s 
				where item_name=%s and item_code=%s""",(qnty,item_name,item_code))
				frappe.msgprint("Kitchen Stock Updated")
			else:
				q3=frappe.db.sql("""select max(cast(name as int)) from `tabKitchen Stock`""")[0][0]
				if q3:
					name=int(q3)+1;
				else:
					name=1	
				q2=frappe.db.sql("""insert into `tabKitchen Stock` set name=%s, item_name=%s, item_code=%s, quantity=%s""",(name,item_name,item_code,qnty))
				frappe.msgprint("New Entry addede in Kitchen Stock.")

	def on_cancel(self):
		ls=self.kitchenreceiver_item
		for i in range(len(ls)):
			item_name=ls[i].item_name
			item_code=ls[i].item_code
			qnty=ls[i].quantity
			q1=frappe.db.sql("""select quantity from `tabKitchen Stock` where item_name=%s and item_code=%s """,(item_name,item_code))
			if q1:
				query=frappe.db.sql("""update `tabKitchen Stock` 
				set quantity=quantity-%s 
				where item_name=%s and item_code=%s""",(qnty,item_name,item_code))
				frappe.msgprint("Kitchen Stock Updated")
			#-------Godown Stock Updation-----------------
			q2=frappe.db.sql("""select quantity from `tabGodown Stock` where item_name=%s and item_code=%s """,(item_name,item_code))
			if q2:
				query=frappe.db.sql("""update `tabGodown Stock` 
				set quantity=quantity+%s 
				where item_name=%s and item_code=%s""",(qnty,item_name,item_code))
				frappe.msgprint("Godown Stock Updated")
@frappe.whitelist()
def get_item_detail(itm):
	q=frappe.db.sql("""select item_name,rate,item_code,uom from `tabItems` where name=%s and item_sub_group='Kitchen Items' and item_group='Purchase Items'""",itm)
	return (q)