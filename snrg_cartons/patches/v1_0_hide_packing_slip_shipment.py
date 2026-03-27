import frappe


def execute():
	"""Hide ERPNext's Packing Slip and Shipment doctypes — replaced by
	Packed Carton and Outward Shipment in the Supply Chain module."""
	for dt in ["Packing Slip", "Shipment"]:
		if frappe.db.exists("DocType", dt):
			frappe.db.set_value("DocType", dt, "hidden", 1)
			frappe.clear_cache(doctype=dt)
