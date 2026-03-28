import frappe


def execute():
	"""Hide ERPNext doctypes superseded by the Supply Chain module:
	• Packing Slip        → replaced by Packed Carton
	• Shipment            → replaced by Outward Shipment
	• Shipment Parcel Template → no equivalent needed
	"""
	for dt in ["Packing Slip", "Shipment", "Shipment Parcel Template"]:
		if frappe.db.exists("DocType", dt):
			frappe.db.set_value("DocType", dt, "hidden", 1)
			frappe.clear_cache(doctype=dt)
