import frappe


def execute():
	"""Hide ERPNext's Shipment Parcel Template — not used in SNRG workflow."""
	if frappe.db.exists("DocType", "Shipment Parcel Template"):
		frappe.db.set_value("DocType", "Shipment Parcel Template", "hidden", 1)
		frappe.clear_cache(doctype="Shipment Parcel Template")
