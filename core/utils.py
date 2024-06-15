# core/utils.py

################################################################################################
# self-explenatory  (function)
################################################################################################

def hex_to_rgba(hex_color, alpha=0.08):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'