def make_SN_plot(fig, cycles, wc, name, color="black"):
    fig.add_scatter(
        x=cycles,
        y=wc.basquin_load(cycles),
        mode="lines",
        name=name + " 50%",
        line_color=color,
    )
    fig.add_scatter(
        x=cycles,
        y=wc.basquin_load(cycles, failure_probability=0.1),
        mode="lines",
        name=name + " 10%",
        line_color=color,
        line_dash="dash",
    )
    fig.add_scatter(
        x=cycles,
        y=wc.basquin_load(cycles, failure_probability=0.9),
        mode="lines",
        name=name + " 90%",
        line_color=color,
        line_dash="dash",
    )
    return fig