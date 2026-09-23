# Copyright (c) 2026, Shenbaga Devi B and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document  # type: ignore[reportMissingImports]
from frappe.model.naming import make_autoname  # type: ignore[reportMissingImports]

class PackagingMaterial(Document):
	def autoname(self):
		self.name=make_autoname(f"{self.material_code.upper()}-PKG-.YYYY.-.####")
	def validate(self):
		if self.charge_to_customer <= self.unit_cost:
			frappe.msgprint("Unit cost should be less than the charge to customer always")