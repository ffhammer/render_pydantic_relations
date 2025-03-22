from typing import List
from pydantic import BaseModel
from render_pydantic_relations import visualize_relationship


class Location(BaseModel):
    city: str
    state: str
    road: str
    house_number: str


class User(BaseModel):
    id: int
    name: str
    friends_user_ids: List[int]
    location: Location


class Post(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    author: User


class Comment(BaseModel):
    id: int
    post_id: int
    user_id: int
    message: str


class Profile(BaseModel):
    id: int
    user_id: int
    bio: str
    user: User


class Like(BaseModel):
    id: int
    post_id: int
    user_id: int


class Group(BaseModel):
    id: int
    name: str
    user_ids: List[int]


if __name__ == "__main__":
    models = [User, Post, Comment, Profile, Like, Group, Location]
    graph = visualize_relationship(models)
    graph.graph_attr.update({"dpi": "300", "rankdir": "LR", "size": "10,5!"})
    graph.render("example", format="png", view=True, cleanup=True)
