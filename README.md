# render_pydantic_relations

Visualize relationships between Pydantic models using Graphviz.

## Install

´´´python
pip install git+https://github.com/ffhammer/render_pydantic_relations.git
´´´

## Usage

´´´python
from render import visualize_relationship
from my_models import User, Order

graph = visualize_relationship([User, Order])
graph.render("out", format="png", cleanup=True)
´´´

