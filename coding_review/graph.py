"""LangGraph wiring only; domain behavior lives in specialist/report modules."""

from langgraph.graph import END, START, StateGraph

from coding_review.agents.aggregator import aggregate_results
from coding_review.agents.prompts import SPECIALTIES
from coding_review.agents.reviewer import make_reviewer
from coding_review.backends.base import ReviewBackend
from coding_review.domain import State


def build_graph(model: ReviewBackend):
    graph = StateGraph(State)
    for name in SPECIALTIES:
        graph.add_node(name, make_reviewer(name, model))
        graph.add_edge(START, name)
    graph.add_node("aggregator", aggregate_results)
    # A list of sources is an explicit barrier: all three must finish first.
    graph.add_edge(list(SPECIALTIES), "aggregator")
    graph.add_edge("aggregator", END)
    return graph.compile()
