import frappe

@frappe.whitelist()
def share_delivery_order(delivery_order_name, user_email):
    frappe.share.add("Delivery Order",delivery_order_name, user_email,read=1)
    return "Delivery Order Shared Successfully"

@frappe.whitelist()
def unsafe_delivery_order():
    return frappe.get_all("Delivery Order",fields=["*"])

@frappe.whitelist()
def safe_delivery_order():
    orders = frappe.get_list("Delivery Order",fields=["name","customer_name","customer_phone","customer_email"])
    if "DP Ops Manager" not in frappe.get_roles(frappe.session.user):
        for i in orders:
            i.pop("customer_phone",None)
            i.pop("customer_email",None)
    return orders