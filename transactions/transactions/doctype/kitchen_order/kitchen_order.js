cur_frm.cscript.onload=function(doc,cdt,cdn)
{

var g_order_id;
	Date.prototype.yyyymmdd = function() 
	{
   	var yyyy = this.getFullYear().toString();
  	var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
   	var dd  = this.getDate().toString();
   	return yyyy +'-'+ (mm[1]?mm:"0"+mm[0]) +'-'+ (dd[1]?dd:"0"+dd[0]); // padding
  	};

	d = new Date();
	m=d.yyyymmdd();
	doc.date=m
	frappe.call({
		method:'transactions.transactions.doctype.kitchen_order.kitchen_order.show_table',
		args:{d:m},
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message)
			set_field_options('test',doclist[0])
			g_tables=doclist[1]
			set_field_options('test1',doclist[2])
			//alert(doclist[3])
			//cur_frm.set_value('waiter_name',doclist[3])
		}
	})

}