// Copyright (c) 2026, Shenbaga Devi B and contributors
// For license information, please see license.txt

frappe.ui.form.on("Delivery Order", {
	setup(frm) {
        frm.set_query("assigned_rider",function(){
            return{
                filters:{
                    status:"Active",
                    assigned_zone:frm.doc.delivery_zone
                }
            }
        });
 	},
    refresh(frm) {
        if (frm.doc.status == "Delivered") {
            frm.dashboard.add_indicator("Delivered","green") 
        }
        else if (frm.doc.status === "Delivery Failed") {
            frm.dashboard.add_indicator("Delivery Failed", "red");
        } 
        else if (frm.doc.status === "In Transit") {
            frm.dashboard.add_indicator("In Transit", "orange");
        }
        if (frm.doc.status=="In Transit" || frm.doc.status=="Re-attempt Scheduled") {
            frm.add_custom_button("Log Delivery Attempt", function() {
                frappe.msgprint("Log Delivery Attempt clicked");
            });
        }
    },
    assigned_rider(frm){
        frappe.db.get_value("Rider",frm.doc.assigned_rider,"assigned_zone",
            r =>{
                if(r.assigned_zone!=frm.doc.delivery_zone){
                    frappe.msgprint("Zone mismatch")
                }
            }
        )
    }
 });

 frappe.ui.form.on("Packaging Usage Entry",{
    quantity(frm,cdt,cdn){
        let row=locals[cdt][cdn]
        let total=row.quantity*row.unit_price
        frappe.model.set_value(cdt,cdn,"total_price",total)
    }
 })