import plotly.graph_objects as go
import plotly.io as pio

class Graph:
    def __init__(self, browser_history, fig):
        self.browser_history = browser_history
        self.fig = fig

    # ("zillow.com", 4) => "zillow.com: 4"
    @staticmethod
    def to_domain_label(datum):
        return "%s: %d" % datum

    @classmethod
    def fromBrowserHistory(cls, browser_history):
        return Graph(browser_history, Graph.get_fig(browser_history))

    def show_fig(self):
        self.fig.show()

    def write_fig_to_html_filepath(self, html_filepath):
        pio.write_html(self.fig, file=html_filepath, auto_open=False)

    @staticmethod
    def get_fig(browser_history):
        domains = list(browser_history.keys())

        # [("zillow", 4)]
        domain_label_data = [(domain, len(browser_history[domain])) for domain in domains]

        # ["zillow: 4"]
        domain_labels = [Graph.to_domain_label(domain_label_datum) for domain_label_datum in domain_label_data]

        destination_labels = ["Viewed Listing: 432", "Considered: 57", "Requested Tour: 22", "Scheduled Tour: 6",
                              "Toured: 3", "Requested Application",
                              "Applied: 8", "Abandoned: 46", "Accepted: 1"]
        labels = domain_labels + destination_labels


        listing_viewed_edges = [
            (
                labels.index(Graph.to_domain_label(domain_datum)),
                labels.index("Viewed Listing: 432"),
                len(browser_history[domain_datum[0]])
            )
            for domain_datum in domain_label_data
        ]
        source_target_value_listing_edges = list(map(list, zip(*listing_viewed_edges)))
        listing_viewed_sources = source_target_value_listing_edges[0]
        listing_viewed_targets = source_target_value_listing_edges[1]
        listing_viewed_values = source_target_value_listing_edges[2]

        listing_viewed_to_considered = (
            labels.index("Viewed Listing: 432"),
            labels.index("Considered: 57"),
            22 + 31  # applied + "not interested" cards in trello
        )  # from trello and gmail

        considered_to_treq = (
            labels.index("Considered: 57"),
            labels.index("Requested Tour: 22"),
            22
        )  # from trello and gmail

        considered_to_not_interested = (
            labels.index("Considered: 57"),
            labels.index("Abandoned: 46"),
            31
        )  # from trello and gmail

        requested_tour_to_scheduled = (
            labels.index("Requested Tour: 22"),
            labels.index("Scheduled Tour: 6"),
            6
        )  # from gcal

        requested_tour_to_abandoned = (
            labels.index("Requested Tour: 22"),
            labels.index("Abandoned: 46"),
            5
        )  # from gcal

        scheduled_to_toured = (
            labels.index("Scheduled Tour: 6"),
            labels.index("Toured: 3"),
            3
        )  # from memory

        scheduled_to_abandoned = (
            labels.index("Scheduled Tour: 6"),
            labels.index("Abandoned: 46"),
            3
        )  # from gcal

        considered_applied = (
            labels.index("Considered: 57"),
            labels.index("Applied: 8"),
            4
        )  # from gmail

        toured_to_applied = (
            labels.index("Toured: 3"),
            labels.index("Applied: 8"),
            3
        )  # from memory

        applied_to_abandoned = (
            labels.index("Applied: 8"),
            labels.index("Abandoned: 46"),
            7
        )  # from memory

        applied_to_accepted = (
            labels.index("Applied: 8"),
            labels.index("Accepted: 1"),
            1
        )  # from memory

        manual_edges = [listing_viewed_to_considered, considered_to_not_interested, considered_applied,
                        considered_to_treq, requested_tour_to_scheduled, requested_tour_to_abandoned,
                        scheduled_to_toured, scheduled_to_abandoned, toured_to_applied, applied_to_accepted, applied_to_abandoned]

        # https://plotly.com/python/sankey-diagram/
        sources = listing_viewed_sources + [manual_edge[0] for manual_edge in manual_edges]
        targets = listing_viewed_targets + [manual_edge[1] for manual_edge in manual_edges]
        values = listing_viewed_values + [manual_edge[2] for manual_edge in manual_edges]

        domain_label_nones = [None for domain_label in domain_labels]
        destination_label_nones = [None for destination_label in range(0, len(destination_labels) - 3)]
        xs = domain_label_nones + destination_label_nones + [0.9, 0.9]
        ys = domain_label_nones + destination_label_nones + [0.1, 0.5]

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color="blue",
                x=xs,
                y=ys

        ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            ))])

        fig.update_layout(title_text="Listings", font_size=14)
        return fig

