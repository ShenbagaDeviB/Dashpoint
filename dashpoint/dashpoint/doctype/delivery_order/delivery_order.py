# Copyright (c) 2026, Shenbaga Devi B and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document  # type: ignore[reportMissingImports]


class DeliveryOrder(Document):
    def validate(self):
        if len(self.customer_phone)!=10:
            frappe.throw("Customer phone number should be 10 digits")
        
        if self.status in ["In Transit","Delivery Failed","Re-attempt Scheduled","Delivered","Escalated"]:
            if not self.assigned_rider:
                frappe.throw("Assigned rider is needed")
        
        if ((self.status=="Delivery Failed") and (self.failure_reason=="No Reason")):
            frappe.throw("Failure reason is mandatory")
        
        packaging_total=0
        for row in self.packaging_usage_entry:
            row.total_price=row.quantity*row.unit_price
            packaging_total+=row.total_price
        self.packaging_total=packaging_total
        
        if not self.delivery_fee:
            self.delivery_fee=frappe.db.get_single_value("Dispatch Settings","default_delivery_fee")
        self.final_amount=self.packaging_total+self.delivery_fee
    
    @frappe.whitelist()
    def record_delivery_attempt(delivery_order_name, outcome, failure_reason=None):
        delivery_order = frappe.get_doc("Delivery Order", delivery_order_name)
        if outcome=="Failed":
            delivery_order.delivery_attempts_count=delivery_order.delivery_attempts_count+1
            maximum_attempts=frappe.db.get_single_value("Dispatch Settings","max_delivery_attempts")
            if delivery_order.delivery_attempts_count<maximum_attempts:
                delivery_order.status="Re-attempt Scheduled"
            else:
                delivery_order.status="Escalated"
        elif outcome=="Delivered":
            delivery_order.status="Delivered"      
            delivery_order.delivered_on=frappe.utils.now()
        delivery_order.save()
        frappe.publish_realtime(
            "delivery_status_changed",
            {
                "delivery_order": delivery_order.name,
                "status": delivery_order.status
            }, 
            user=delivery_order.owner)
   
    def before_submit(self):
        if self.status!="Delivered":
            frappe.throw("It will be submitted only when the status is Delivered")
            
        for material in self.packaging_usage_entry:
            stock_qty=frappe.db.get_value("Packaging Material",material.material,"stock_quantity")
            if stock_qty<material.quantity:
                frappe.throw("Insufficient Stock!!! "
                    f"Stock for {material.material}: "
                    f"Required Quantity:{material.quantity}. "
                    f"Available:{stock_qty} ")
    
    def on_submit(self):
        for qty in self.packaging_usage_entry:
            instock=frappe.db.get_value("Packaging Material",qty.material,"stock_quantity")
            frappe.db.set_value("Packaging Material",qty.material,"stock_quantity",instock-qty.quantity)
            
        receipt=frappe.get_doc({
			"doctype":"Delivery Receipt",
            "delivery_order":self.name
		})
        receipt.insert()
        frappe.enqueue("dashpoint.dashpoint.doctype.delivery_order.delivery_order.send_delivery_confirmation"
                       ,delivery_order=self.name
                       )
    
    def on_cancel(self):
        self.status="Cancelled"
        for row in self.packaging_usage_entry:
            material=frappe.get_doc("Packaging Material",row.material)
            material.stock_quantity+=row.quantity
            material.save()
        receipt=frappe.db.get_value("Delivery Receipt",{"delivery_order":self.name},"name")
        if receipt:
            frappe.get_doc("Delivery Receipt",receipt).cancel()
    def on_trash(self):
        if self.status not in ["Cancelled","Draft"]:
            frappe.throw("You cannot delete the order until it is draft/cancelled")
    
    def on_update(self):
        pass
def send_delivery_confirmation(delivery_order):
		rec=frappe.get_doc("Delivery Order",delivery_order)
		frappe.sendmail(
            recipients=[rec.customer_email],
            subject="Delivery Confirmation Mail",
            message=f"Your delivery for {rec.name} is completed..!!"
        )