import matplotlib.pyplot as plt


def single_graph(df, x_col, y_col):
    title = f'{x_col} vs {y_col}'
    plt.figure(figsize=(14, 8))

    params = {"text.color": "midnightblue",
              "xtick.color": "black",
              "ytick.color": "black"}
    plt.rcParams.update(params)

    plt.plot(df[x_col], df[y_col], 'midnightblue')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)

    plt.show()

    return