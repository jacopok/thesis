if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    from matplotlib import patheffects

    white_stroke = [patheffects.withStroke(linewidth=4, foreground="w")]

    text = plt.text(0.5, 0.5, 'Hello')
    text.set_path_effects(white_stroke)

    plt.show()