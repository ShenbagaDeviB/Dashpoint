### Dashpoint 

### C3 – Rename a Test Rider Record

We have a Rider DocType with the naming series RDR-.####.
We also have a Delivery Order DocType. 
In Delivery Order, assigned_rider is a Link field connected to the Rider DocType.
For example: If a Rider record is: RDR-0005 and we rename it to: RDR-0005 Rename
The new name will also be updated in the assigned_rider field of the Delivery Order.
This happens because assigned_rider is a Link field connected to the Rider DocType. 
Frappe automatically updates the linked record when the Rider is renamed.

### D2 – Why is frappe.get_all dangerous in a whitelisted method exposed to low-privilege users?
First, what is a whitelisted method?
A whitelisted method is a method that can be called from the client or user side.
Then, what is frappe.get_all?
frappe.get_all is used to fetch records. But it does not check the user's permissions.
Because of this, a low-privilege user may be able to see data that they are not allowed to access.
This can cause unauthorized data access.
To avoid this, we can use frappe.get_list. It also fetches records, but it applies the user's permissions.

### E1-The Recursion Pitfall

on_update() is called whenever a document is updated.
If we call self.save() inside on_update(), it triggers the update process again.
This calls on_update() again.
This creates an infinite loop /recursion.
It causes a RecursionError and the process may crash.
So, avoid using self.save() inside on_update().
If we need to update a field, we can update the field directly

### E2-merge=True

We don't use merge=True because it merges both old and new name.

### E3-One Performance Judgment Call

We choose frappe.db.get_value because we only need low stock threshold.
We didn't need entire Dispatch Settings.
We will be directly fetch our requirements through frappe.db.get_value.

### B2c - Document Lifecycle Bugs

1.self.save() inside validate() can cause a recursion pitfall, where it runs again and again. So, self.save() should be avoided to prevent unnecessary loops.
2.Running stock updation inside validate() means every time validation is called, the stock update also runs. This can cause repeated stock updates and lead to unusual/incorrect values.
So, we have to avoid self.save() and stock updation inside validate().

### B2d - Optimistic Locking

Same document is edited by two different staff. The first person saves the changes, and those changes are stored. If the second person tries to save, Frappe throws an error saying “Document has been modified after you opened it.” Frappe checks the modified timestamp to detect this and prevents the second save from overwriting the first person’s changes.

### H1- Why does a frappe.call inside the validate client event not work, and why must async fetches happen in onload/refresh instead?

frappe.call() is an async function, in which we get the response later.
So, validate() happens just before the save. If we write frappe.call() inside validate(), we get the response after the validation is over.
Then comes onload() and refresh(). These run when we open or refresh the form, so we can use frappe.call() here to fetch the data.

### K2-Spot the N+1

# N+1 PROBLEM - fix this
orders = frappe.get_all("Delivery Order", fields=["name","assigned_rider"])
for o in orders:
    rider = frappe.get_doc("Rider", o.assigned_rider)
    print(rider.rider_name, rider.phone)

If we have 10 orders we have 10+1 --> 11 queries.
First of all we collect every rider details and the total rider details.
So it may cause n+1 problem.
So avoid querying inside the loop. 
First bulk fetching then use loop.

orders = frappe.get_all("Delivery Order", fields=["name","assigned_rider"])
riders = frappe.get_all("Rider",fields=["name","rider_name","phone"])

for o in orders:
    for rider in riders:
        if o.assigned_rider==rider.name:
            print(rider.rider_name,rider.phone)

### N1 — ignore_permissions Audit & JS-Hiding Pitfall
def on_submit(self):
    for qty in self.packaging_usage_entry:
        instock=frappe.db.get_value("Packaging Material",qty.material,"stock_quantity")
        frappe.db.set_value("Packaging Material",qty.material,"stock_qty",instock-qty.quantity,ignore_permissions=True)

We used ignore_permissions=True here because this operation is performed automatically by the system, not directly by the user.

if (!frappe.user.has_role("DP Ops Manager")) {
    frm.set_df_property("customer_phone", "hidden", 1);
}

If not DP Ops Manager hide customer_phone if DP Ops Manager then shows it. It is not a security we can still access it through API.