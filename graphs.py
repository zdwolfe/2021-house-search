import plotly.graph_objects as go


def generate_graph(browser_history):
    domains = list(browser_history.keys())
    destination_labels = ["Viewed Listing", "Requested Tour", "Scheduled Tour", "Toured", "Requested Application", "Applied", "Rejected",
                          "Accepted"]
    labels = domains + destination_labels

    viewed_listing_index = labels.index("Viewed Listing")
    listing_viewed_edges = [
        (labels.index(domain), viewed_listing_index, len(browser_history[domain])) for domain in domains
    ]
    source_target_value_listing_edges = list(map(list, zip(*listing_viewed_edges)))
    listing_viewed_sources = source_target_value_listing_edges[0]
    listing_viewed_targets = source_target_value_listing_edges[1]
    listing_viewed_values = source_target_value_listing_edges[2]

    # https://plotly.com/python/sankey-diagram/
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color="blue"
        ),
        link=dict(
            source=listing_viewed_sources,
            target=listing_viewed_targets,
            value=listing_viewed_values
        ))])

    fig.update_layout(title_text="Listings", font_size=14)
    fig.show()
