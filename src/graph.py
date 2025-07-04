from langgraph.graph import StateGraph

from nodes.transit import (
    fetch_transit_alerts,
    geocode_and_find_station,
    render_response,
)
from state import TransitState

g = StateGraph(TransitState)
g.add_node("geo", geocode_and_find_station)
g.add_node("alerts", fetch_transit_alerts)
g.add_node("render", render_response)

g.set_entry_point("geo")
g.add_edge("geo", "alerts")
g.add_edge("alerts", "render")

app = g.compile()
