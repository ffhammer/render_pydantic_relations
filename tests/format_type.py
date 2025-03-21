from typing import Optional, Union, List, Set, Dict, Tuple
from render_pydantic_relations.core import format_type


def test_format_type() -> None:
    assert format_type(int) == "int"
    assert (
        format_type(Optional[str]) == "Union[str, NoneType]"
    ), f"got {format_type(Optional[str])}"
    assert (
        format_type(Union[int, str]) == "Union[int, str]"
    ), f"got {format_type(Union[int, str])}"
    assert format_type(List[int]) == "list[int]", f"got {format_type(List[int])}"
    assert format_type(Set[str]) == "set[str]", f"got {format_type(Set[str])}"
    assert (
        format_type(Dict[str, int]) == "dict[str, int]"
    ), f"got {format_type(Dict[str, int])}"
    assert (
        format_type(Tuple[int, str, float]) == "tuple[int, str, float]"
    ), f"got {format_type(Tuple[int, str, float])}"
    # Nested types
    assert (
        format_type(List[Optional[int]]) == "list[Union[int, NoneType]]"
    ), f"got {format_type(List[Optional[int]])}"
    assert (
        format_type(Dict[str, List[Optional[int]]])
        == "dict[str, list[Union[int, NoneType]]]"
    ), f"got {format_type(Dict[str, List[Optional[int]]])}"
    print("All tests passed.")


if __name__ == "__main__":
    test_format_type()
