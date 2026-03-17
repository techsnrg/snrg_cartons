import frappe
import base64
import io


@frappe.whitelist()
def get_code128_barcode(text):
	"""Generate a Code 128 barcode as a base64-encoded PNG data URI.
	This can be called from Jinja templates in print formats."""
	try:
		import barcode
		from barcode.writer import ImageWriter
		
		code128 = barcode.get_barcode_class('code128')
		buffer = io.BytesIO()
		writer = ImageWriter()
		writer.set_options({
			'module_height': 6,
			'module_width': 0.25,
			'quiet_zone': 2,
			'font_size': 0,
			'text_distance': 0,
			'write_text': False
		})
		bc = code128(str(text), writer=writer)
		bc.write(buffer)
		buffer.seek(0)
		img_base64 = base64.b64encode(buffer.read()).decode()
		return f"data:image/png;base64,{img_base64}"
	except ImportError:
		# python-barcode not installed, generate a simple SVG barcode
		return _generate_svg_barcode(text)
	except Exception:
		return ""


def _generate_svg_barcode(text):
	"""Fallback: generate Code 128 barcode as inline SVG data URI."""
	# Code 128B encoding
	PATTERNS = [
		"11011001100", "11001101100", "11001100110", "10010011000", "10010001100",
		"10001001100", "10011001000", "10011000100", "10001100100", "11001001000",
		"11001000100", "11000100100", "10110011100", "10011011100", "10011001110",
		"10111001100", "10011101100", "10011100110", "11001110010", "11001011100",
		"11001001110", "11011100100", "11001110100", "11101101110", "11101001100",
		"11100101100", "11100100110", "11101100100", "11100110100", "11100110010",
		"11011011000", "11011000110", "11000110110", "10100011000", "10001011000",
		"10001000110", "10110001000", "10001101000", "10001100010", "11010001000",
		"11000101000", "11000100010", "10110111000", "10110001110", "10001101110",
		"10111011000", "10111000110", "10001110110", "11101110110", "11010001110",
		"11000101110", "11011101000", "11011100010", "11011101110", "11101011000",
		"11101000110", "11100010110", "11101101000", "11101100010", "11100011010",
		"11101111010", "11001000010", "11110001010", "10100110000", "10100001100",
		"10010110000", "10010000110", "10000101100", "10000100110", "10110010000",
		"10110000100", "10011010000", "10011000010", "10000110100", "10000110010",
		"11000010010", "11001010000", "11110111010", "11000010100", "10001111010",
		"10100111100", "10010111100", "10010011110", "10111100100", "10011110100",
		"10011110010", "11110100100", "11110010100", "11110010010", "11011011110",
		"11011110110", "11110110110", "10101111000", "10100011110", "10001011110",
		"10111101000", "10111100010", "11110101000", "11110100010", "10111011110",
		"10111101110", "11101011110", "11110101110", "11010000100", "11010010000",
		"11010011100", "1100011101011",
	]
	
	START_B = 104
	STOP = 106
	
	codes = [START_B]
	checksum = START_B
	for i, ch in enumerate(str(text)):
		val = ord(ch) - 32
		codes.append(val)
		checksum += val * (i + 1)
	codes.append(checksum % 103)
	codes.append(STOP)
	
	# Build bar pattern
	bars = ""
	for c in codes:
		bars += PATTERNS[c]
	
	# Generate SVG
	bar_width = 1.5
	height = 25
	width = len(bars) * bar_width + 20
	
	svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
	svg += f'<rect width="{width}" height="{height}" fill="white"/>'
	x = 10
	for bit in bars:
		if bit == '1':
			svg += f'<rect x="{x}" y="0" width="{bar_width}" height="{height}" fill="black"/>'
		x += bar_width
	svg += '</svg>'
	
	svg_b64 = base64.b64encode(svg.encode()).decode()
	return f"data:image/svg+xml;base64,{svg_b64}"
