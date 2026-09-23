import frappe

def rename_doc(old_name,new_name):
    frappe.rename_doc("Rider",old_name,new_name,merge=False)