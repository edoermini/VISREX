from PyQt6.QtGui import QColor

def is_dark_theme_active(qt_element):

    # Check the color role for the WindowText color
    background_color = qt_element.palette().color(qt_element.backgroundRole())

    # Calculate the overall brightness of the color
    brightness = (background_color.red() * 299 + background_color.green() * 587 + background_color.blue() * 114) / 1000

    # If the brightness is less than a threshold, consider it a dark theme
    return brightness < 128

def make_color_darker(color:QColor, factor=0.8):
    """
    Make a QColor darker by adjusting the RGB values.

    Parameters:
    - color: The original QColor.
    - factor: A factor between 0 and 1 to control the darkness level.
    """
    red = int(color.red() * factor)
    green = int(color.green() * factor)
    blue = int(color.blue() * factor)

    return QColor(red, green, blue)

def is_light_color(color: QColor):

    # Calculate the luminance using the formula: Y = 0.299*R + 0.587*G + 0.114*B
    luminance = 0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()

    # Choose the text color based on the luminance
    return luminance > 128