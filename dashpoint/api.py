import frappe
from frappe.query_builder import DocType  # type: ignore[reportMissingImports]
from frappe.query_builder.functions import Now  # type: ignore[import-not-found]

@frappe.whitelist()
def get_stuck_deliveries():
    DO=DocType("Delivery Order")
    result = (frappe.qb.from_(DO)
        .select(DO.name, DO.customer_name, DO.assigned_rider, DO.creation)
        .where(
            (DO.status.isin(["In Transit", "Re-Attempt Scheduled"]))
            & (DO.creation < frappe.utils.add_days(frappe.utils.now_datetime(), -2))
        )
        .orderby(DO.creation)
        .run(as_dict=True))
    return result

def reassign_zone(from_rider,to_rider):
    try:
        frappe.db.sql(""" UPDATE `tabDelivery Order` SET assigned_rider =%s 
                      WHERE assigned_rider =%s AND status='In Transit' """,(to_rider,from_rider))
        frappe.db.commit()
    except:
        frappe.db.rollback()
        frappe.log_error(
            frappe.get_traceback(),
            "Reassign Zone Failed"
        )
        raise

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