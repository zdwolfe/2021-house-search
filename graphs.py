import plotly.graph_objects as go


# ("zillow.com", 4) => "zillow.com: 4"
def domain_label(datum):
    return "%s: %d" % datum

def generate_graph(browser_history):
    domains = list(browser_history.keys())

    # [("zillow", 4)]
    domain_label_data = [(domain, len(browser_history[domain])) for domain in domains]

    # ["zillow: 4"]
    domain_labels = [domain_label(domain_label_datum) for domain_label_datum in domain_label_data]

    destination_labels = ["Viewed Listing", "Requested Tour", "Scheduled Tour", "Toured", "Requested Application",
                          "Applied", "Rejected", "Accepted"]
    labels = domain_labels + destination_labels

    viewed_listing_index = labels.index("Viewed Listing")

    listing_viewed_edges = [
        (
            labels.index(domain_label(domain_datum)),
            viewed_listing_index,
            len(browser_history[domain_datum[0]])
        )
        for domain_datum in domain_label_data
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
