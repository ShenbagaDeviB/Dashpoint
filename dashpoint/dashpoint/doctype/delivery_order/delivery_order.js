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
    }
    
 });