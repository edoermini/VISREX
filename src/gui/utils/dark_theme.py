def isDarkThemeActive(qt_element):

    # Check the color role for the WindowText color
    background_color = qt_element.palette().color(qt_element.backgroundRole())

    # Calculate the overall brightness of the color
    brightness = (background_color.red() * 299 + background_color.green() * 587 + background_color.blue() * 114) / 1000

    # If the brightness is less than a threshold, consider it a dark theme
    return brightness < 128