# -*- coding: utf-8 -*-
# Copyright (c) 2015, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class KitchenOrder(Document):
	pass

@frappe.whitelist()
def show_table(d):
	q=frappe.db.sql("""select table_no from `tabTable`""")
	l_rm=frappe.db.sql("""select b.room_no from `tabBooking` b where b.flag=1""")
	room_length = len(l_rm)
	l=len(q)
	dict={}
	l_tbl=''
	str1=''
	q13 = frappe.db.sql("""select order_status from `tabParcel Item` where table_no='Parcel' and order_status='Running' and date=%s""",(d))
	if q13:
		str4="""
			<input type="hidden" name="d" id="d" value="%s">
			<button class="btn btn-primary" tabindex="1" id="btnParcel" type="button" value="Parcel"
			onclick=parcelFunction(this.value)
			>Parcel</button>""" %(d)
	else:
		str4="""
			<input type="hidden" name="d" id="d" value="%s">
			<button class="btn btn-info" tabindex="1" id="btnParcel" type="button" value="Parcel"
			onclick=parcelFunction(this.value)
			>Parcel</button>""" %(d)
	for j in range(0, room_length):
		tbl='L-'+l_rm[j][0]
		q12 = frappe.db.sql("""select order_status from `tabLodge Item` where table_no=%s and order_status='Running' and date=%s""",(tbl,d))
		if (len(q12) > 0):
			str3="""
			<input type="hidden" name="d" id="d" value="%s">
			<button class="btn btn-primary" tabindex="1" id="btnL-%s" type="button" value=L-%s     
			onclick=lodgeFunction(this.value)
			>L-%s</button>""" %(d,l_rm[j][0],l_rm[j][0],l_rm[j][0])
			l_tbl=l_tbl+str3
		else:
			str3="""
			<input type="hidden" name="d" id="d" value="%s">
			<button class="btn btn-warning" tabindex="1" id="btnL-%s" type="button" value=L-%s     
			onclick=lodgeFunction(this.value)
			>L-%s</button>""" %(d,l_rm[j][0],l_rm[j][0],l_rm[j][0])
			l_tbl=l_tbl+str3
	for i in range(0, l):
		q11 = frappe.db.sql("""select order_status from `tabOrder Item` where table_no=%s and order_status='Running' and date=%s""",(q[i][0],d))
		if (len(q11) > 0):
			str2="""
			<input type="hidden" name="d" id="d" value="%s">
			<button class="btn btn-primary" tabindex="1" id="btn%s" type="button" value=%s     
			onclick=myFunction(this.value)
			>%s</button>""" %(d,q[i][0],q[i][0],q[i][0])
			str1=str1+str2
		else:
			str2="""
			<input type="hidden" name="d" id="d" value="%s">
			<button class="btn btn-success" tabindex="1" id="btn%s" type="button" value=%s     
			onclick=myFunction(this.value)
			>%s</button>""" %(d,q[i][0],q[i][0],q[i][0])
			str1=str1+str2
	
	html="""
		<html>
			<head>
				<script>
					function lodgeFunction(x)
					{
					var btn = x;
					document.getElementById("table_no").value = btn;
					document.getElementById("shifttable").style.visibility = "visible";
					document.getElementById("checkbill").style.visibility = "visible";
					var date=document.getElementById('d').value;
					frappe.call
						({
							method:'transactions.transactions.doctype.kitchen_order.kitchen_order.get_bill_no',
							args:{},
							callback:function(r)
							{
								var o = parseInt(r.message)+parseInt(1);
								cur_frm.set_value('order_id',o);
								document.getElementById("order_id").value= o ;
								cur_frm.set_value('waiter_name','')
								frappe.call({
									method:'transactions.transactions.doctype.kitchen_order.kitchen_order.current_lodge_table',
									args:{date:date,o:o,tbl:btn},
									callback:function(r)
									{
										var doclist1=frappe.model.sync(r.message);
										set_field_options('test3',doclist1[1]);
										cur_frm.set_value('order_id',doclist1[0]);
										document.getElementById("order_id").value=doclist1[0];
									}
								})
							}
						})
					}
					function parcelFunction(x)
					{
						var btn = x;
						var date=document.getElementById('d').value;
						var tbl = x;
						var wtr = 0;
						document.getElementById("table_no").value= btn;
						document.getElementById("shifttable").style.visibility = "hidden";
						document.getElementById("checkbill").style.visibility = "hidden";
						frappe.call
						({
							method:'transactions.transactions.doctype.kitchen_order.kitchen_order.get_order_id',
							args:{date:date,tbl:tbl,wtr:wtr,btn:btn},
							callback:function(r)
							{
								
								cur_frm.set_value('waiter_name','')
								var doclist1=frappe.model.sync(r.message);
								set_field_options('test3',doclist1[1]);
								cur_frm.set_value('order_id',doclist1[0]);
								document.getElementById("order_id").value=doclist1[0];
							}
						})
					}
					function myFunction(x)
					{
						document.getElementById("shifttable").style.visibility = "visible";
						document.getElementById("checkbill").style.visibility = "visible";
						var date=document.getElementById('d').value;
						var id=x;
						var tbl;
						var wtr;
						frappe.call({
								method:'transactions.transactions.doctype.kitchen_order.kitchen_order.get_info',
								args:{id1:id,date:date},
								callback:function(r)
								{
									var doclist=frappe.model.sync(r.message);
									//cur_frm.set_value("table_no",doclist[0][0][1]);
									cur_frm.set_value("waiter_name",doclist[0][0][0]);
									//cur_frm.set_value('order_status','Running');
									//cur_frm.set_value('is_lodge_client','');
									//cur_frm.set_value('select_room','');
									//cur_frm.set_value('customer_name','');
									//document.getElementById("date").value=date;
									document.getElementById("waiter_name").value=doclist[0][0][0];
									document.getElementById("order_status").value='Running';
									document.getElementById("table_no").value=doclist[0][0][1];
									var w=doclist[0][0][0];
									var t=doclist[0][0][1];
									var date=doclist[1];
									var btn = 0;
									frappe.call
									({
										method:'transactions.transactions.doctype.kitchen_order.kitchen_order.get_order_id',
										args:{date:date,tbl:t,wtr:w,btn:btn},
										callback:function(r)
										{
											var doclist1=frappe.model.sync(r.message);
											set_field_options('test3',doclist1[1]);
											cur_frm.set_value('order_id',doclist1[0]);
											document.getElementById("order_id").value=doclist1[0];
										}
									})
								}
							});
					}
				</script>
			</head>
		</html>
	"""
	q=frappe.db.sql("""select name,item_code from `tabItems` where item_group='Sale Items'""")
	form="""
		<html>
		<body>

		<input type="hidden" name="order" id="order_id">
		<input type="hidden" name="waiter" id="waiter_name">
		<input type="hidden" name="orderstatus" id="order_status">
		<input type="hidden" name="table" id="table_no">

		<div>
			Item: &nbsp;<select style="width:175px" tabindex="2" name="item" id="item" onblur="selectitem()"">"""

	opt=''
	for i in range(len(q)):
		options1="""<option value="%s.%s">%s</option>""" %(q[i][0],q[i][1],q[i][1])
		opt=opt+options1
	form1="""</select>
  			&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
 	 		Quantity:&nbsp;
  			<input type="text" tabindex="3" name="quantity" id="quantity">
  			&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
 	 		Counter Stock:&nbsp;
  			<input type="text" readonly name="c_stock" id="c_stock">
  		</div><br>
  		<div>
  			Rate: 
  			<input type="text" tabindex="4" name="rate"  id="rate" onblur="calculateamount()">
  			&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  			Amount: &nbsp;
  			<input type="text" tabindex="5" name="amount" id="amount">
  		</div><br>
  			<input type="button" tabindex="6" value="Add Item" id="submit" onclick="additem()">
  			<input type="button" tabindex="7" value="Shift Table" id="shifttable" onclick="shift_table()">
  			<input type="button" tabindex="8" value="Cancel Order" id="cancelorder" onclick="cancel_order()">
  			<input type="button" tabindex="9" value="Check Bill" id="checkbill" onclick="check_bill()">
  			<input type="button" tabindex="10" value="Print Bill" id="printbill" onclick="print_bill()">
		</body>
		</html>

	"""
	
	script="""
		<html>
			<head>
				<script>
				function check_bill()
				{
					var t = document.getElementById("table_no").value;
					var d = document.getElementById("d").value;
					var order_id = document.getElementById("order_id").value;
					var w = document.getElementById("waiter_name").value;
					frappe.call({
						method:'transactions.transactions.doctype.kitchen_order.kitchen_order.get_new_div',
						args:{d:d,tbl:t,wtr:w,order_id:order_id},
						callback:function(r)
						{
							var doclist=frappe.model.sync(r.message);
  							set_field_options('test3',doclist[0]);
  							var length1=doclist[1];
  							var divToPrint1=document.getElementById('d1');
        					var col =1;
        					if (isNaN(col) || col == "") 
        					{
        						alert("Invalid Column");
               					 return;
            				}
        					col = parseInt(col, 10);
        					col = col - 1;
        					var tbl = document.getElementById("Tbl1");
         					if (tbl != null) 
         					{
         						if (col < 0 || col >= tbl.rows.length - 1) 
         						{
			   						alert("Invalid Column");
               						return;
           						}
        						for (var i = 0; i < tbl.rows.length; i++) 
        						{
        		 					for (var j = 0; j < tbl.rows[i].cells.length; j++) 
        		 						{
                    						tbl.rows[i].cells[j].style.display = "";
                     						if (j == col)
                     						tbl.rows[i].cells[j].style.display = "none";
                  						}
            					}

         					}
  							newWin= window.open("");
  							//newWin.document.write(divToPrint.outerHTML);
  							newWin.document.write(divToPrint1.outerHTML);
 							newWin.print();
  							newWin.close();
						}
					})
				}
				function print_bill()
				{
					var tbl = t = document.getElementById("table_no").value;
					var d = document.getElementById("d").value;
					var o_id = order_id = document.getElementById("order_id").value;
					var wtr = w = document.getElementById("waiter_name").value;

					var a= "btn"+tbl;
					document.getElementById(a).className="btn btn-success";
					if (tbl=='Parcel')
					{
						frappe.call({
							method:'transactions.transactions.doctype.kitchen_order.kitchen_order.parcel_record_submission',
							args:{d:d,o_id:o_id},
							callback:function()
							{
								cur_frm.set_value('order_status','Completed');
							}
						})
					}
					else
					{
						frappe.call({
							method:'transactions.transactions.doctype.kitchen_order.kitchen_order.record_submission',
							args:{d:d,tbl:tbl,wtr:wtr,o_id:o_id},
							callback:function()
							{
								cur_frm.set_value('order_status','Completed');
							}
						})
					}
					frappe.call({
						method:'transactions.transactions.doctype.kitchen_order.kitchen_order.get_div',
						args:{d:d,tbl:t,wtr:w,order_id:order_id},
						callback:function(r)
						{
							var doclist=frappe.model.sync(r.message);
  							set_field_options('test3',doclist[0]);
  							var length1=doclist[1];
  							var divToPrint1=document.getElementById('d1');
        					var col =1;
        					if (isNaN(col) || col == "") 
        					{
        						alert("Invalid Column");
               					 return;
            				}
        					col = parseInt(col, 10);
        					col = col - 1;
        					var tbl = document.getElementById("Tbl1");
         					if (tbl != null) 
         					{
         						if (col < 0 || col >= tbl.rows.length - 1) 
         						{
			   						alert("Invalid Column");
               						return;
           						}
        						for (var i = 0; i < tbl.rows.length; i++) 
        						{
        		 					for (var j = 0; j < tbl.rows[i].cells.length; j++) 
        		 						{
                    						tbl.rows[i].cells[j].style.display = "";
                     						if (j == col)
                     						tbl.rows[i].cells[j].style.display = "none";
                  						}
            					}

         					}
  							newWin= window.open("");
  							//newWin.document.write(divToPrint.outerHTML);
  							newWin.document.write(divToPrint1.outerHTML);
 							newWin.print();
  							newWin.close();
						}
					})
				}
				function cancel_order()
				{
					var t = document.getElementById("table_no").value;
					var d = document.getElementById("d").value;
					var order_id = document.getElementById("order_id").value;
					var w = document.getElementById("waiter_name").value;
					if(t=='Parcel')
					{
						frappe.call({
							method:'transactions.transactions.doctype.kitchen_order.kitchen_order.cancel_parcel_order',
							args:{t:t,d:d,order_id:order_id,w:w},
							callback:function(r)
							{	
								var doclist1 = frappe.model.sync(r.message)
								set_field_options('test3',doclist1[0]);
								var a = doclist1[1];
								var x = "btn"+a;
								document.getElementById(x).className="btn btn-success";
								refresh_fields('test');
							}
						})
					}
					else
					{
						var n = t.search("L-")
						if (n==0)
						{
							frappe.call({
								method:'transactions.transactions.doctype.kitchen_order.kitchen_order.cancel_lodge_order',
								args:{t:t,d:d,order_id:order_id,w:w},
								callback:function(r)
								{	
									var doclist1 = frappe.model.sync(r.message)
									set_field_options('test3',doclist1[0]);
									var a = doclist1[1];
									var x = "btn"+a;
									document.getElementById(x).className="btn btn-success";
									refresh_fields('test');
								}
							})
						}
						else
						{	
							frappe.call({
								method:'transactions.transactions.doctype.kitchen_order.kitchen_order.cancel_table_order',
								args:{t:t,d:d,order_id:order_id,w:w},
								callback:function(r)
								{	
									var doclist1 = frappe.model.sync(r.message)
									set_field_options('test3',doclist1[0]);
									var a = doclist1[1];
									var x = "btn"+a;
									document.getElementById(x).className="btn btn-success";
									refresh_fields('test');
								}
							})
						}
					}
				}
				function shift_table()
				{
				var t = document.getElementById("table_no").value;
				var d = document.getElementById("d").value;
				var order_id = document.getElementById("order_id").value;
				var w = document.getElementById("waiter_name").value;
				var shift_table_no = prompt("Please enter table no");
				if(shift_table_no!=null)
				{
					
					frappe.call({
						method:'transactions.transactions.doctype.kitchen_order.kitchen_order.shift_table_no',
						args:{t:t,d:d,order_id:order_id,w:w,shift_table_no:shift_table_no},
						callback:function(r)
						{
							var doc=frappe.model.sync(r.message);
							prbtn=doc[0];
							nbtn=doc[1];
							prbtn1='btn'+prbtn;
							var n = nbtn.search("L-")
							if (n==0)
							{
								nbtn1='btn'+nbtn
							}
							else
							{
								nbtn1='btn'+nbtn;
							}
							document.getElementById(prbtn1).className="btn btn-success";
							document.getElementById(nbtn1).className="btn btn-primary";
							refresh_fields('test');
							//window.location.reload();
						}
					})
				}
				}
				function selectitem()
				{
					var item = document.getElementById('item').value;
					var itm = item.split(".");
					var item_id = itm[0]
					var item_code = itm[1]
					frappe.call({
						method:'transactions.transactions.doctype.kitchen_order.kitchen_order.get_counter_stock',
						args:{item_id:item_id,item_code:item_code},
						callback:function(r)
							{
								var doclist1=frappe.model.sync(r.message);
								document.getElementById('rate').value = doclist1[0];
								if(doclist1[1]==null)
								{
									document.getElementById('c_stock').value = '';
								}
								else
								{
									document.getElementById('c_stock').value = doclist1[1];
								}
							}
						})
				}
				function calculateamount()
				{
					var a=document.getElementById("rate").value;
					var b=document.getElementById("quantity").value;
					var c =  (a*b);
					document.getElementById("amount").value = c;
				}
				function additem()
				{
					var o_id = document.getElementById('order_id').value;
					var w = document.getElementById('waiter_name').value;
					var o_sts = document.getElementById('order_status').value;
					var item = document.getElementById('item').value;
					var qty= document.getElementById('quantity').value;
					var rate = document.getElementById("rate").value;
					var d = document.getElementById('d').value;
					var t = document.getElementById("table_no").value;
					var amt = document.getElementById("amount").value;
					var itm = item.split(".");
					var item_id = itm[0]
					var item_code = itm[1]
					var a = "btn"+t
					document.getElementById(a).className="btn btn-primary";
					document.getElementById("item").focus();
					var n = t.search("L-")
					if (t=='Parcel')
					{
						frappe.call({
							method:'transactions.transactions.doctype.kitchen_order.kitchen_order.insert_parcel_item',
							args:{o:o_id,i:item_id,item_code:item_code,q:qty,r:rate,amt:amt,d:d,tbl:t,o_sts:o_sts},
							callback:function(r)
							{
								set_field_options('test3',r.message)
								document.getElementById('quantity').value = '';
								document.getElementById('rate').value = '';
								document.getElementById('c_stock').value = '';
								document.getElementById('amount').value = '';
							}
						})
					}
					else
					{
						//var n = t.search("L-")
						//if (n==0)
						//{
						//}
							frappe.call({
							method:'transactions.transactions.doctype.kitchen_order.kitchen_order.insert_item',
							args:{o:o_id,i:item_id,item_code:item_code,q:qty,r:rate,amt:amt,d:d,tbl:t,w:w,o_sts:o_sts},
							callback:function(r)
								{
									set_field_options('test3',r.message)
									document.getElementById('quantity').value = '';
									document.getElementById('rate').value = '';
									document.getElementById('c_stock').value = '';
									document.getElementById('amount').value = '';
								}
							})
						
					}
				}
				function delete_item(y)
				{
					var arr=[];
					var a=y;
					var row=document.getElementById(a);
					var i=row.getElementsByTagName('td');	
					var j=i.length;
					for(k=0;k<j-1;k++)
						{
							var cell=i[k].innerHTML;
							arr.push(cell);
						}
					var item_name=arr[1]
					var qty=arr[2]
					var amt=arr[3]
					var t = document.getElementById("table_no").value;
					if(t=='Parcel')
					{
						frappe.call
						({
							method:'transactions.transactions.doctype.kitchen_order.kitchen_order.delete_parcel_item',
							args:{x:arr[0],item_name:item_name,qty:qty},
							callback:function(r)
							{
								set_field_options('test3',r.message);
							}
						})
					}
					else
					{
						var n = t.search("L-")
						if (n==0)
						{
							
							frappe.call
							({
								method:'transactions.transactions.doctype.kitchen_order.kitchen_order.delete_lodge_item',
								args:{x:arr[0],item_name:item_name,qty:qty},
								callback:function(r)
								{
									set_field_options('test3',r.message);
								}
							})
						}
						else
						{
							frappe.call
							({
								method:'transactions.transactions.doctype.kitchen_order.kitchen_order.delete_order_item',
								args:{x:arr[0],item_name:item_name,qty:qty},
								callback:function(r)
								{
									set_field_options('test3',r.message);
								}
							})
						}
					}
				}
				
				</script>
			</head>
		</html>
	""" 
	com=html+str1+l_tbl+str4
	f=form+opt+form1
	com1=(script+f)
	return (com,l,com1)
@frappe.whitelist()
def current_lodge_table(date,o,tbl):
	q0=frappe.db.sql("""select max(order_id) from `tabLodge Item` where table_no=%s and date=%s and order_status='Running' limit 1""",(tbl,date))[0][0]
	if q0:
			o=q0
			a=''
			q=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabLodge Item` 
			where order_id=%s and table_no=%s and order_status='Running'""",(o,tbl))
			l=len(q)
			t_amt=0
			for i in range(0, l):
				m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(q[i][5]))
				if(q[i][3]==0):
					html_str="""
					<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,q[i][0],m1[0][0],q[i][2],q[i][3],q[i][4],i,i,i)
					a=a+html_str
					t_amt=t_amt+q[i][4]
				else:
					html_str="""
					<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,q[i][0],m1[0][0],q[i][2],q[i][3],q[i][4],i,i,i)
					a=a+html_str
					t_amt=t_amt+q[i][4]
			ttl_str="""
			<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
			table=(show_list()+a+ttl_str)
			o_id = o
			return (o_id,table,t_amt)
	else:
			o_id = int(get_bill_no())+int(1)
			return (o_id,show_list())
@frappe.whitelist()
def insert_parcel_item(o,i,item_code,q,r,amt,d,tbl,o_sts):
	#-----Update Counter Stock----------------------------
	q14 = frappe.db.sql("""select item_sub_group from `tabItems` where name=%s""",(i))
	if (q14[0][0]=='Kitchen Items'):
		#Do Nothing
		aaa=0;
	else:
		q13= frappe.db.sql("""select quantity from `tabCounter Stock` where item_code=%s""",(item_code))[0][0]
		if (int(q13) >= int(q)):
			q14 = frappe.db.sql("""update `tabCounter Stock` set quantity = quantity-%s where item_code=%s""",(q,item_code))
		else:
			frappe.throw("No Counter Stock available")
	#-----Inserting Record in `tabParcel Item`-------------
	a=''
	q12=frappe.db.sql("""select max(cast(name as int)) from `tabParcel Item`""")[0][0]
	if q12:
		n=int(q12)+1
	else:
		n=1
	q = frappe.db.sql("""insert into `tabParcel Item` set name=%s, order_id=%s, item=%s, item_code=%s, quantity=%s, rate=%s, amount=%s, 
		date=%s, table_no=%s,order_status=%s""",(n,o,i,item_code,q,r,amt,d,tbl,"Running"))
	#------Dispalting HTML table----------------------------
	m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabParcel Item` where order_id=%s""",(o))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(m[i][5]))
		if(m[i][3]==0):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			t_amt=t_amt+int(m[i][4])
			a=a+html_str
		else:
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			a=a+html_str
			t_amt=t_amt+int(m[i][4])
	ttl_str="""
	<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return (show_list()+a+ttl_str)
@frappe.whitelist()
def get_new_div(d,tbl,wtr,order_id):
	str11="""
	<style>
		#n1{
		display:none;
		}
		#n2{
		display:none;
		}
		#n3{
		display:none;
		}
		#n4{
		display:none;
		}
	</style>
	<div id='d1' align=center>
	
	<table id="Tbl1">
	
	
	<tr align=center><td width=150 id='n2'>Name</td><td width=200 >Item</td>
	<td width=100 >Qty</td><td width=100 >Rate</td></tr>
	""" 
	a=''
	x = "L-" in str(tbl)
	if (x==True):
		m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabLodge Item` where order_id=%s and order_status='Running'""",(order_id))
	else:
		m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabOrder Item` where order_id=%s and order_status='Running'""",(order_id))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(m[i][5]))
		if(m[i][3]==0):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3])
			t_amt=t_amt+int(m[i][4])
			a=a+html_str
		else:
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3])
			a=a+html_str
			t_amt=t_amt+int(m[i][4])
	#ttl_str="""
	#<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return(str11+a,l)

@frappe.whitelist()
def get_div(d,tbl,wtr,order_id):
	str11="""
	<style>
		#n1{
		display:none;
		}
		#n2{
		display:none;
		}
		#n3{
		display:none;
		}
		#n4{
		display:none;
		}
	</style>
	<div id='d1' align=center>
	<h3>Hotel Amrit Residency</h3>
	<h5>Opp. LIC Office,Gandhi Nagar,Nanded</h5>
	<h5>Contact No:(02462)-223438,220438</h5>
	<table id="Tbl1">
	<tr align=left><td></td><td colspan="2">Date:%s</td><td colspan="3">Table No:%s</td></tr>
	<tr align=left><td></td><td colspan="2">Order No:%s</td><td colspan="3">Waiter Name:%s</td></tr>
	<tr align=center><td width=150 id='n2'>Name</td><td width=200 >Item</td>
	<td width=100 >Qty</td><td width=100 >Rate</td><td width=100 >Amount</td></tr>
	""" %(d,tbl,order_id,wtr)
	a=''
	if (tbl=='Parcel'):
		m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabParcel Item` where order_id=%s""",(order_id))
	else:
		x = "L-" in str(tbl)
		if (x==True):
			#-----Getting Record in `tabLodge Item`-------------
			m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabLodge Item` where order_id=%s and order_status='Running'""",(order_id))
		else:
			#-----Getting Record in `tabLodge Item`-------------
			m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabOrder Item` where order_id=%s and order_status='Running'""",(order_id))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(m[i][5]))
		if(m[i][3]==0):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4])
			t_amt=t_amt+int(m[i][4])
			a=a+html_str
		else:
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4])
			a=a+html_str
			t_amt=t_amt+int(m[i][4])
	ttl_str="""
	<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return(str11+a+ttl_str,l)

@frappe.whitelist()
def print_order_bill():
	frappe.msgprint("hi")

@frappe.whitelist()
def cancel_lodge_order(t,d,order_id,w):
	q = frappe.db.sql("""select item,item_code,quantity from `tabLodge Item` where order_id=%s""",(order_id))
	for i in range (len(q)):
		item = q[i][0]
		item_code = q[i][1]
		qty = q[i][2]
		q1 = frappe.db.sql("""update `tabCounter Stock` set quantity=quantity+%s where item_code=%s""",(qty,item_code))
	q2 = frappe.db.sql("""delete from `tabLodge Item` where order_id=%s""",(order_id))
	a = show_list()
	return (a,t) 

@frappe.whitelist()
def cancel_parcel_order(t,d,order_id,w):
	q = frappe.db.sql("""select item,item_code,quantity from `tabParcel Item` where order_id=%s""",(order_id))
	for i in range (len(q)):
		item = q[i][0]
		item_code = q[i][1]
		qty = q[i][2]
		q1 = frappe.db.sql("""update `tabCounter Stock` set quantity=quantity+%s where item_code=%s""",(qty,item_code))
	q2 = frappe.db.sql("""delete from `tabParcel Item` where order_id=%s""",(order_id))
	a = show_list()
	return (a,t) 

@frappe.whitelist()
def cancel_table_order(t,d,order_id,w):
	q = frappe.db.sql("""select item,item_code,quantity from `tabOrder Item` where order_id=%s""",(order_id))
	for i in range (len(q)):
		item = q[i][0]
		item_code = q[i][1]
		qty = q[i][2]
		q1 = frappe.db.sql("""update `tabCounter Stock` set quantity=quantity+%s where item_code=%s""",(qty,item_code))
	q2 = frappe.db.sql("""delete from `tabOrder Item` where order_id=%s""",(order_id))
	a = show_list()
	return (a,t) 
@frappe.whitelist()
def shift_table_no(t,d,order_id,w,shift_table_no):
	y = "L-" in str(t) 
	if (y==True):
		#-------------shift from lodge to table------------------------
		q2 = frappe.db.sql("""select date,item,item_code,quantity,rate,amount,total_amount,waiter_name,order_status from `tabLodge Item` where date=%s and order_id=%s""",(d,order_id)) 
		for i in range (len(q2)):
			q12=frappe.db.sql("""select max(cast(name as int)) from `tabOrder Item`""")[0][0]
			if q12:
				n=int(q12)+1
			else:
				n=1
			q = frappe.db.sql("""insert into `tabOrder Item` set name=%s, date=%s, item=%s, item_code=%s,quantity=%s,
				rate=%s, amount=%s, total_amount=%s, waiter_name=%s, order_status=%s, table_no=%s,order_id=%s""",(n,q2[i][0],q2[i][1],q2[i][2],q2[i][3],q2[i][4],q2[i][5],q2[i][6],q2[i][7],q2[i][8],shift_table_no,order_id))
		q3 = frappe.db.sql("""delete from `tabLodge Item` where order_id=%s""",(order_id))
	x = "L-" in str(shift_table_no)
	if (x==True):
		#-------------shift from table to lodge------------------------
		q2 = frappe.db.sql("""select date,item,item_code,quantity,rate,amount,total_amount,waiter_name,order_status from `tabOrder Item` where date=%s and order_id=%s""",(d,order_id)) 
		for i in range (len(q2)):
			q12=frappe.db.sql("""select max(cast(name as int)) from `tabLodge Item`""")[0][0]
			if q12:
				n=int(q12)+1
			else:
				n=1
			q = frappe.db.sql("""insert into `tabLodge Item` set name=%s, date=%s, item=%s, item_code=%s,quantity=%s,
				rate=%s, amount=%s, total_amount=%s, waiter_name=%s, order_status=%s, table_no=%s,order_id=%s""",(n,q2[i][0],q2[i][1],q2[i][2],q2[i][3],q2[i][4],q2[i][5],q2[i][6],q2[i][7],q2[i][8],shift_table_no,order_id))
		q3 = frappe.db.sql("""delete from `tabOrder Item` where order_id=%s""",(order_id))
	else:
		#-------------shift from table to table------------------------
		q1 = frappe.db.sql("""select waiter from `tabAssignTableData` where date=%s and table_no=%s""",(d,shift_table_no))[0]
		wtr = q1[0]
		q = frappe.db.sql("""update `tabOrder Item` set table_no=%s ,waiter_name=%s where order_id=%s""",(shift_table_no,wtr,order_id))
	return (t,shift_table_no)

@frappe.whitelist()
def parcel_record_submission(d,o_id):
	#----------------------------------------------------------
	total_amt=frappe.db.sql("""select sum(amount) from `tabParcel Item` where order_id=%s""",(o_id))[0][0]
	q=frappe.db.sql("""update `tabParcel Item` set total_amount=%s where
	date=%s and order_id=%s """,(total_amt,d,o_id))

@frappe.whitelist()
def record_submission(d,tbl,wtr,o_id):
	x = "L-" in str(tbl)
	if (x==True):
		r=tbl.split("-")
		q1=frappe.db.sql("""select customer_name from `tabBooking` where room_no=%s""",(r[1]))
		#-----Updating Record in `tabLodge Item`-------------
		total_amt=frappe.db.sql("""select sum(amount) from `tabLodge Item` where order_id=%s""",(o_id))[0][0]
		q=frappe.db.sql("""update `tabLodge Item` set order_status='Completed',total_amount=%s,customer_name=%s,select_room=%s where
		date=%s and table_no=%s and order_id=%s """,(total_amt,q1[0][0],r[1],d,tbl,o_id))
	else:
		#-----Updating Record in `tabOrder Item`-------------
		total_amt=frappe.db.sql("""select sum(amount) from `tabOrder Item` where order_id=%s""",(o_id))[0][0]
		q=frappe.db.sql("""update `tabOrder Item` set order_status='Completed' ,total_amount=%s where
		date=%s and table_no=%s and waiter_name=%s and order_id=%s """,(total_amt,d,tbl,wtr,o_id))

@frappe.whitelist()
def delete_parcel_item(x,item_name,qty):
	q0=frappe.db.sql("""select item,quantity,order_id from `tabParcel Item` where name=%s""",(x))
	if q0:
		q1= frappe.db.sql("""update `tabCounter Stock` set quantity=quantity+%s where item_name=%s""",(qty,item_name))
	sql=frappe.db.sql("""delete from `tabParcel Item` where name=%s and order_status='Running'""",(x))
	#------Dispalting HTML table----------------------------
	a=''
	m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabParcel Item` where order_id=%s""",(q0[0][2]))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(m[i][5]))
		if(m[i][3]==0):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			t_amt=t_amt+int(m[i][4])
			a=a+html_str
		else:
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			a=a+html_str
			t_amt=t_amt+int(m[i][4])
	ttl_str="""
	<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return (show_list()+a+ttl_str)

@frappe.whitelist()
def delete_lodge_item(x,item_name,qty):
	q0=frappe.db.sql("""select item,quantity,order_id from `tabLodge Item` where name=%s""",(x))
	if q0:
		q1= frappe.db.sql("""update `tabCounter Stock` set quantity=quantity+%s where item_name=%s""",(qty,item_name))
	sql=frappe.db.sql("""delete from `tabLodge Item` where name=%s and order_status='Running'""",(x))
	#------Dispalting HTML table----------------------------
	a=''
	m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabLodge Item` where order_id=%s""",(q0[0][2]))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(m[i][5]))
		if(m[i][3]==0):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			t_amt=t_amt+int(m[i][4])
			a=a+html_str
		else:
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			a=a+html_str
			t_amt=t_amt+int(m[i][4])
	ttl_str="""
	<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return (show_list()+a+ttl_str)

@frappe.whitelist()
def delete_order_item(x,item_name,qty):
	q0=frappe.db.sql("""select item,quantity,order_id from `tabOrder Item` where name=%s""",(x))
	if q0:
		q1= frappe.db.sql("""update `tabCounter Stock` set quantity=quantity+%s where item_name=%s""",(qty,item_name))
	sql=frappe.db.sql("""delete from `tabOrder Item` where name=%s and order_status='Running'""",(x))
	#------Dispalting HTML table----------------------------
	a=''
	m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabOrder Item` where order_id=%s and order_status='Running'""",(q0[0][2]))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(m[i][5]))
		if(m[i][3]==0):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			t_amt=t_amt+int(m[i][4])
			a=a+html_str
		else:
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			a=a+html_str
			t_amt=t_amt+int(m[i][4])
	ttl_str="""
	<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return (show_list()+a+ttl_str)

@frappe.whitelist()
def get_counter_stock(item_id,item_code):
	q1 = frappe.db.sql("""select item_sub_group from `tabItems` where name=%s""",(item_id))
	if (q1[0][0]=='Kitchen Items'):
		#Do Nothing
		q = frappe.db.sql("""select i.rate from `tabItems` i where i.name= %s""",(item_id))[0]
		return q
	else:
		q = frappe.db.sql("""select i.rate,c.quantity from `tabCounter Stock` c ,`tabItems` i where c.item_code=%s and i.name= %s""",(item_code,item_id))
		if q:
			return q[0]
		else:
			frappe.throw("No Counter Stock Available for Seletec Item")

@frappe.whitelist()
def insert_item(o,i,item_code,q,r,amt,d,tbl,w,o_sts):
	#-----Update Counter Stock----------------------------
	q14 = frappe.db.sql("""select item_sub_group from `tabItems` where name=%s""",(i))
	if (q14[0][0]=='Kitchen Items'):
		#Do Nothing
		aaa=0;
	else:
		q13= frappe.db.sql("""select quantity from `tabCounter Stock` where item_code=%s""",(item_code))[0][0]
		if (int(q13) >= int(q)):
			q14 = frappe.db.sql("""update `tabCounter Stock` set quantity = quantity-%s where item_code=%s""",(q,item_code))
		else:
			frappe.throw("No Counter Stock available")
	#------Lodge or Table-----------------------
	x = "L-" in str(tbl)
	if (x==True):
		#-----Inserting Record in `tabLodge Item`-------------
		a=''
		q12=frappe.db.sql("""select max(cast(name as int)) from `tabLodge Item`""")[0][0]
		if q12:
			n=int(q12)+1
		else:
			n=1
		q11=frappe.db.sql("""insert into `tabLodge Item` set name=%s,order_id=%s,item=%s,item_code=%s,quantity=%s,rate=%s,amount=%s,
		date=%s,table_no=%s,waiter_name=%s,order_status=%s""",(n,o,i,item_code,q,r,amt,d,tbl,w,"Running"))
		m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabLodge Item` where order_id=%s and order_status='Running'""",(o))
	else:
		#-----Inserting Record in `tabOrder Item`-------------
		a=''
		q12=frappe.db.sql("""select max(cast(name as int)) from `tabOrder Item`""")[0][0]
		if q12:
			n=int(q12)+1
		else:
			n=1
		q11=frappe.db.sql("""insert into `tabOrder Item` set name=%s,order_id=%s,item=%s,item_code=%s,quantity=%s,rate=%s,amount=%s,
		date=%s,table_no=%s,waiter_name=%s,order_status=%s""",(n,o,i,item_code,q,r,amt,d,tbl,w,"Running"))
		m=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabOrder Item` where order_id=%s and order_status='Running'""",(o))
	#------Dispalting HTML table----------------------------
	l=len(m)
	t_amt=0
	for i in range(0, l):
		m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(m[i][5]))
		if(m[i][3]==0):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			t_amt=t_amt+int(m[i][4])
			a=a+html_str
		else:
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m1[0][0],m[i][2],m[i][3],m[i][4],i,i,i)
			a=a+html_str
			t_amt=t_amt+int(m[i][4])
	ttl_str="""
	<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return (show_list()+a+ttl_str)


def show_list():
	header="""
	<style>
		#n1{
		display:none;
		}
		#n2{
		display:none;
		}
	</style>
	<table border=1 id="Tbl1">
	<tr align=center><td width=150 id='n2'>Name</td><td width=200 >Item</td>
	<td width=100>Qty</td><td width=100>Rate</td><td width=100 >Amount</td><td width=35>X</td></tr>""" 
	html_function="""
				<html>
					<head>
						<script>
							function delete_record(y)
							{
								var arr=[];
								var a=y;
								var row=document.getElementById(a);
								var i=row.getElementsByTagName('td');	
								var j=i.length;
								for(k=0;k<j-1;k++)
								{
									var cell=i[k].innerHTML;
									arr.push(cell);
								}
								var brand=arr[1]
								var type=arr[2]
								var qty=arr[3]
								frappe.call
								({
									method:'transactions.transactions.doctype.kot.kot.delete_order_item',
									args:{x:arr[0],brand:brand,type1:type,qty:qty},
									callback:function(r)
									{
										set_field_options('test1',r.message);
									}
								})
							}
						</script>
					</head>
				</html>
			"""

	return (header+html_function)
@frappe.whitelist()
def get_bill_no():
	par = frappe.db.sql("""select max(order_id) from `tabParcel Item`""")[0]
	if (par==(None,)):
		par='0'
	else:
		par = par[0]
	ldg = frappe.db.sql("""select max(order_id) from `tabLodge Item`""")[0]
	if (ldg==(None,)):
		ldg='0'
	else:
		ldg = ldg[0]
	tbl = frappe.db.sql("""select max(order_id) from `tabOrder Item`""")[0]
	if (tbl==(None,)):
		tbl='0'
	else:
		tbl = tbl[0]
	bill_no = o = max(int(par),int(ldg),int(tbl))
	return(bill_no)

@frappe.whitelist()
def get_order_id(date,tbl,wtr,btn):
	x = "Parcel" in str(tbl)
	if (x==True):
		q0=frappe.db.sql("""select max(order_id) from `tabParcel Item` where table_no=%s and date=%s and order_status='Running' limit 1""",(tbl,date))[0][0]
		if q0:
			o=int(q0)
			a=''
			q=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabParcel Item` 
			where order_id=%s and date=%s and table_no=%s and order_status='Running'""",(o,date,tbl))
			l=len(q)
			t_amt=0
			for i in range(0, l):
				m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(q[i][5]))
				if(q[i][3]==0):
					html_str="""
					<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,q[i][0],m1[0][0],q[i][2],q[i][3],q[i][4],i,i,i)
					a=a+html_str
					t_amt=t_amt+q[i][4]
				else:
					html_str="""
					<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,q[i][0],m1[0][0],q[i][2],q[i][3],q[i][4],i,i,i)
					a=a+html_str
					t_amt=t_amt+q[i][4]
			ttl_str="""
			<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
			table=(show_list()+a+ttl_str)
			o_id = o
			return (o_id,table,t_amt)
		else:
			#q=frappe.db.sql("""select max(order_id) from `tabOrder Item`""")[0][0]
			#if q:
			#	o=int(q)+1
			#else:
			#	o=1
			o_id = int(get_bill_no())+int(1)
			return (o_id,show_list())
	else:
		q0=frappe.db.sql("""select max(order_id) from `tabOrder Item` where table_no=%s and date=%s and order_status='Running' limit 1""",(tbl,date))[0][0]
		if q0:
			o=int(q0)
			a=''
			q=frappe.db.sql("""select name,item_code,quantity,rate,amount,item from `tabOrder Item` 
			where order_id=%s and date=%s and table_no=%s and order_status='Running'""",(o,date,tbl))
			l=len(q)
			t_amt=0
			for i in range(0, l):
				m1=frappe.db.sql("""select item_name from `tabItems` where name=%s""",(q[i][5]))
				if(q[i][3]==0):
					html_str="""
					<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,q[i][0],m1[0][0],q[i][2],q[i][3],q[i][4],i,i,i)
					a=a+html_str
					t_amt=t_amt+q[i][4]
				else:
					html_str="""
					<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_item(this.value)><font color='red'>x</button></td></tr>""" %(i,q[i][0],m1[0][0],q[i][2],q[i][3],q[i][4],i,i,i)
					a=a+html_str
					t_amt=t_amt+q[i][4]
			ttl_str="""
			<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
			table=(show_list()+a+ttl_str)
			o_id = o
			return (o_id,table,t_amt)
		else:
			#q=frappe.db.sql("""select max(order_id) from `tabOrder Item`""")[0][0]
			#if q:
			#	o=int(q)+1
			#else:
			#	o=1
			o_id = int(get_bill_no())+int(1)
			return (o_id,show_list())

@frappe.whitelist()
def get_info(id1,date):
	q1=frappe.db.sql("""select waiter,table_no from `tabAssignTableData` where date=%s and table_no=%s""",(date,id1))
	return q1,date

