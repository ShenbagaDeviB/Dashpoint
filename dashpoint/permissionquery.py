import frappe

def delivery_order_query(user=None):
    user = user or frappe.session.user
    if "DP Ops Manager" in frappe.get_roles(user):
        return ""
    if "DP Rider" in frappe.get_roles(user):
        return f"`tabDelivery Order`.assigned_rider in (select name from `tabRider` where user={frappe.db.escape(user)})"
    return "1=0"