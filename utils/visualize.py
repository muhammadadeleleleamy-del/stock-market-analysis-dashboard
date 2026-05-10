import plotly.graph_objects as go

def plot_stock(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Close"],
        mode="lines",
        name="Close Price"
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Stock Price Trend",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified"
    )

    return fig
