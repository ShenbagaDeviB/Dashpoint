# Copyright (c) 2026, Shenbaga Devi B and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document # type: ignore[reportMissingImports]
from frappe.model.naming import make_autoname # type: ignore[reportMissingImports]

class DeliveryReceipt(Document):
	def autoname(self):
		self.receipt_number = make_autoname("DR-.YYYY.-.#####")
		self.name = self.receipt_number
