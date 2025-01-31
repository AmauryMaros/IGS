def lighter_colors(base_color, num_colors):
    """
    Generate a list of progressively lighter colors based on a given base color.

    Parameters:
    -----------
    base_color : str
        A hex color code representing the base color.
        It should start with a '#' followed by six hexadecimal digits.
        
    num_colors : int
        The number of lighter color variations to generate. Must be a positive integer.

    Returns:
    --------
    list of str
        A list containing the hex color codes of the progressively lighter colors.
        Each color is represented as a hex string.

    """

    # Convert the base color to its RGB components
    r = int(base_color[1:3], 16)
    g = int(base_color[3:5], 16)
    b = int(base_color[5:7], 16)

    # Calculate the step values for degrading
    r_step = (255 - r) / num_colors
    g_step = (255 - g) / num_colors
    b_step = (255 - b) / num_colors

    # Generate the progressively lighter colors
    lighter_colors = []
    for i in range(num_colors):
        new_r = int(r + i * r_step)
        new_g = int(g + i * g_step)
        new_b = int(b + i * b_step)
        lighter_colors.append(f'#{new_r:02X}{new_g:02X}{new_b:02X}')

    return lighter_colors
