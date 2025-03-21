from typing import get_type_hints, List, Tuple, Union, Type
from graphviz import Digraph
from pydantic import BaseModel


def format_type(ftype: type) -> str:
    if getattr(ftype, "__origin__", ftype) not in [
        Union,
        list,
        set,
        dict,
        tuple,
    ] or not getattr(ftype, "__args__", None):
        return ftype.__name__
    args = ", ".join(format_type(arg) for arg in ftype.__args__)
    return f"{ftype.__origin__.__name__}[{args}]"


def render_model(model: Type[BaseModel]) -> Digraph:
    name = model.__name__
    hints = get_type_hints(model)
    label = (
        f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0">'
        f'<TR><TD BGCOLOR="lightgrey" COLSPAN="3"><B>{name}</B></TD></TR>'
    )
    for fname, ftype in hints.items():
        label += (
            f"<TR>"
            f'<TD ALIGN="LEFT">{fname}</TD>'
            f'<TD BGCOLOR="black" WIDTH="1"></TD>'
            f'<TD PORT="{fname}" ALIGN="LEFT">{format_type(ftype)}</TD>'
            f"</TR>"
        )
    label += "</TABLE>>"
    g = Digraph()
    g.node(name, label=label, shape="plaintext")
    return g


def find_edges(models: List[Type[BaseModel]]) -> List[Tuple[str, str, str, str]]:
    names = [model.__name__ for model in models]
    if len(set(names)) != len(names):
        raise ValueError("Model names must be unique.")
    edges: List[Tuple[str, str, str, str]] = []
    for model in models:
        source = model.__name__
        hints = get_type_hints(model)
        for fname, ftype in hints.items():
            if fname.endswith("_id"):
                target_candidates = [
                    n for n in names if fname.endswith(f"{n.lower()}_id")
                ]
                if target_candidates:
                    edges.append((source, fname, target_candidates[0], "references"))
                else:
                    print(
                        f"Warning: No target found for field '{fname}' in model '{source}'."
                    )
            elif fname.endswith("_ids"):
                target_candidates = [
                    n for n in names if fname.endswith(f"{n.lower()}_ids")
                ]
                if target_candidates:
                    edges.append((source, fname, target_candidates[0], "references"))
                else:
                    print(
                        f"Warning: No target found for field '{fname}' in model '{source}'."
                    )

            if isinstance(ftype, type) and issubclass(ftype, BaseModel):
                edges.append((source, fname, ftype.__name__, "contains"))
            elif hasattr(ftype, "__args__") and any(
                isinstance(arg, type) and issubclass(arg, BaseModel)
                for arg in ftype.__args__
            ):
                for arg in (
                    arg
                    for arg in ftype.__args__
                    if isinstance(arg, type) and issubclass(arg, BaseModel)
                ):
                    edges.append((source, fname, arg.__name__, "contains"))
    return edges


def visualize_relationship(models: List[Type[BaseModel]]) -> Digraph:
    """
    Visualize relationships between Pydantic models.

    Constructs a Graphviz Digraph where each node represents a Pydantic model.
    Relationships are determined by two rules:
      1. Containment: A field whose type is a BaseModel (or a container including a BaseModel)
         implies the model "contains" that type.
      2. Reference: A field name ending with "lowername_id" or "lowername_ids" (with lowername being
         the lower case target model's name) indicates a reference to that target model.

    Args:
        models: A list of unique Pydantic BaseModel classes.

    Returns:
        A Graphviz Digraph visualizing the relationships among the provided models.
    """
    graph = Digraph()
    for model in models:
        graph.subgraph(render_model(model))
    for source, port, target, rel_label in find_edges(models):
        graph.edge(
            source,
            target,
            tailport=f"{port}:e",
            style="dashed" if rel_label == "references" else "solid",
        )
    return graph
