"""2026-10-21: scan concurrent colour writers in every shipped programme."""

import pytest
from qlctool.capabilities_of import capabilities_of
from qlctool.checks.build_show_graph import build_show_graph
from qlctool.checks.group_fixtures import group_fixtures
from qlctool.checks.room_states import room_states
from qlctool.checks.rule_collision import check_collisions
from qlctool.fixture_library import FixtureLibrary
from qlctool.workspace import Workspace
from rig_root import RIG_ROOT


@pytest.mark.parametrize("name", ("Vibra.qxw", "Vibra-beats.qxw", "Vibra-split.qxw"))
def test_2026_10_21_no_concurrent_colour_collision_in_any_programme(name):
    workspace = Workspace.load(RIG_ROOT / "QLC+ Setups" / name)
    library = FixtureLibrary.load()
    graph = build_show_graph(workspace.root, capabilities_of(workspace.root, library))
    groups = group_fixtures(workspace.root)
    states = room_states(workspace.root, graph, groups)
    all_functions = {function_id: "programme" for function_id in graph.functions}

    collections = sum(
        function.get("Type") == "Collection" for function in graph.functions.values()
    )
    assert collections > 200
    assert not check_collisions(graph, groups, all_functions, states), name
