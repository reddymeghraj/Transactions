cur_frm.cscript.select_item = function(doc,cdt,cdn)
{
	var d= locals[cdt][cdn]
	var itm = d.select_item;
	frappe.call({
		method :'transactions.transactions.doctype.kitchen_receiver.kitchen_receiver.get_item_detail',
		args:{itm},
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message)
			d.item_name = doclist[0][0];
			d.item_code = doclist[0][2];
			refresh_field('kitchen_receiver_item')
			var item_name = d.item_name;
			var item_code = d.item_code;
			frappe.call({
				method:'transactions.transactions.doctype.counter_receiver.counter_receiver.get_godown_stock',
				args:{item_name,item_code},
				callback:function(r)
				{
					d.current_godown_stock = r.message;
					refresh_field('kitchen_receiver_item');
				}
			})
		}
	})


}
cur_frm.fields_dict["kitchen_receiver_item"].grid.get_field("select_item").get_query = function(doc,cdt,cdn) {
	var child=locals[cdt][cdn];
	var item1=child.item_name;
	return {
		filters: {
			'item_name': item1,
			'item_group':'Purchase Items',
			'item_sub_group':'Kitchen Items'
		}
	}
}