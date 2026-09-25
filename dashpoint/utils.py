import frappe

def rename_doc(old_name,new_name):
    frappe.rename_doc("Rider",old_name,new_name,merge=False)
    
@frappe.whitelist()
def reassign_rider(delivery_order_name, new_rider):
    doc = frappe.get_doc("Delivery Order", delivery_order_name)
    doc.assigned_rider = new_rider
    doc.save()
    return "Rider reassigned successfully"