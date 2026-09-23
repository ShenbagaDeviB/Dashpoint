Dashpoint 

C3 – Rename a Test Rider Record

We have a Rider DocType with the naming series RDR-.####.
We also have a Delivery Order DocType. 
In Delivery Order, assigned_rider is a Link field connected to the Rider DocType.
For example: If a Rider record is: RDR-0005 and we rename it to: RDR-0005 Rename
The new name will also be updated in the assigned_rider field of the Delivery Order.
This happens because assigned_rider is a Link field connected to the Rider DocType. 
Frappe automatically updates the linked record when the Rider is renamed.

D2 – Why is frappe.get_all dangerous in a whitelisted method exposed to low-privilege users?
First, what is a whitelisted method?
A whitelisted method is a method that can be called from the client or user side.
Then, what is frappe.get_all?
frappe.get_all is used to fetch records. But it does not check the user's permissions.
Because of this, a low-privilege user may be able to see data that they are not allowed to access.
This can cause unauthorized data access.
To avoid this, we can use frappe.get_list. It also fetches records, but it applies the user's permissions.
