# -*- coding: utf-8 -*-
# Copyright (c) 2015, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CounterReceiver(Document):
	def on_submit(self):
		date=self.date
		ls=self.counter_receiver_item
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
			#-------Counter Stock Updation-----------------
			q4=frappe.db.sql("""select quantity from `tabCounter Stock` where item_name=%s and item_code=%s """,(item_name,item_code))
			if q4:
				query=frappe.db.sql("""update `tabCounter Stock` 
				set quantity=quantity+%s 
				where item_name=%s and item_code=%s""",(qnty,item_name,item_code))
				frappe.msgprint("Counter Stock Updated")
			else:
				q3=frappe.db.sql("""select max(cast(name as int)) from `tabCounter Stock`""")[0][0]
				if q3:
					name=int(q3)+1;
				else:
					name=1	
				q2=frappe.db.sql("""insert into `tabCounter Stock` set name=%s, item_name=%s, item_code=%s, quantity=%s""",(name,item_name,item_code,qnty))
				frappe.msgprint("New Entry addede in Counter Stock.")

	def on_cancel(self):
		ls=self.counter_receiver_item
		for i in range(len(ls)):
			item_name=ls[i].item_name
			item_code=ls[i].item_code
			qnty=ls[i].quantity
			q1=frappe.db.sql("""select quantity from `tabCounter Stock` where item_name=%s and item_code=%s """,(item_name,item_code))
			if q1:
				query=frappe.db.sql("""update `tabCounter Stock` 
				set quantity=quantity-%s 
				where item_name=%s and item_code=%s""",(qnty,item_name,item_code))
				frappe.msgprint("Counter Stock Updated")
			#-------Godown Stock Updation-----------------
			q2=frappe.db.sql("""select quantity from `tabGodown Stock` where item_name=%s and item_code=%s """,(item_name,item_code))
			if q2:
				query=frappe.db.sql("""update `tabGodown Stock` 
				set quantity=quantity+%s 
				where item_name=%s and item_code=%s""",(qnty,item_name,item_code))
				frappe.msgprint("Godown Stock Updated")

@frappe.whitelist()
def get_godown_stock(item_name,item_code):
	q = frappe.db.sql("select quantity from `tabGodown Stock` where item_name=%s and item_code=%s",(item_name,item_code))
	if q:
		return (q[0][0])
	else:
		frappe.throw("NO Stock Available in Godown")
		return (0)

