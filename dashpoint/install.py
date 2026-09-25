import frappe

def after_install():
    zones = ["North Zone", "Central Zone", "South Zone"]

    for zone in zones:
        if not frappe.db.exists("Delivery Zone", zone):
            doc = frappe.get_doc({
                "doctype": "Delivery Zone",
                "zone_name": zone
            })
            doc.insert()
        if not frappe.db.exists("Dispatch Settings"):
            settings = frappe.get_doc({
                "doctype": "Dispatch Settings",
                "ops_manager_email": "abc@gmail.com"
            })
            settings.insert()
        frappe.msgprint("Dashpoint installed successfully")