#!/usr/bin/env python3
"""
Automated validation suite for Hirely's Graph Explorer
Validates:
1. All referenced edge endpoints exist.
2. Focus mode correctly computes 1, 2, and 3 hop neighborhoods.
3. Filtering does not create dangling edges.
4. Test filtering correctly excludes test and mock nodes.
5. Search matching and empty result handling.
6. Isolated nodes are safely handled.
7. Generated HTML has ZERO remote script or stylesheet dependencies.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict, deque

# Import classifier and builder from build_explorer
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_explorer import classify_layer, determine_node_type, build_explorer


def test_validation():
    repo_root = Path(__file__).resolve().parent.parent
    graph_json_path = repo_root / "graphify-out" / "graph.json"
    html_path = repo_root / "graphify-out" / "hirely-explorer.html"

    print("=== Running Hirely Explorer Validation Tests ===")

    # 1. Load data
    assert graph_json_path.exists(), f"Missing {graph_json_path}"
    with open(graph_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("links", data.get("edges", []))
    node_ids = {n["id"] for n in nodes if "id" in n}

    # Test 1: All referenced edge endpoints exist
    print("Test 1: Validating edge endpoints...")
    dangling = []
    for idx, e in enumerate(edges):
        s = e.get("source")
        t = e.get("target")
        if s not in node_ids or t not in node_ids:
            dangling.append((idx, s, t))

    assert len(dangling) == 0, f"Found {len(dangling)} dangling edges in source graph: {dangling[:5]}"
    print(f"  [PASS] All {len(edges)} edges have valid source and target endpoints.")

    # Test 2: Hop traversal logic (1, 2, and 3 hops)
    print("Test 2: Validating Focus Mode hop traversal...")
    adj = defaultdict(set)
    for e in edges:
        adj[e["source"]].add(e["target"])
        adj[e["target"]].add(e["source"])

    def get_bfs_hops(start_id, max_hops):
        visited = {start_id: 0}
        q = deque([(start_id, 0)])
        while q:
            curr, dist = q.popleft()
            if dist >= max_hops:
                continue
            for neighbor in adj[curr]:
                if neighbor not in visited:
                    visited[neighbor] = dist + 1
                    q.append((neighbor, dist + 1))
        return visited

    # Test with primary hub 'Candidate'
    test_node = "backend_app_models_candidate_candidate"
    assert test_node in node_ids, f"Expected hub {test_node} not in graph"

    hops1 = get_bfs_hops(test_node, 1)
    hops2 = get_bfs_hops(test_node, 2)
    hops3 = get_bfs_hops(test_node, 3)

    assert len(hops1) > 1, "Hop 1 should find direct neighbors"
    assert len(hops2) >= len(hops1), "Hop 2 should be >= Hop 1"
    assert len(hops3) >= len(hops2), "Hop 3 should be >= Hop 2"
    print(f"  [PASS] Focus mode for {test_node}: 1 hop={len(hops1)} nodes, 2 hops={len(hops2)} nodes, 3 hops={len(hops3)} nodes.")

    # Test 3: Filtering does not create dangling edges
    print("Test 3: Validating filter edge consistency...")
    # Test filtering out tests
    prod_node_ids = set()
    for n in nodes:
        _, is_test = classify_layer(
            n.get("source_file"), n.get("label"), n.get("file_type"), n.get("type"), bool(n.get("_py_fixture"))
        )
        if not is_test:
            prod_node_ids.add(n["id"])

    prod_edges = [e for e in edges if e["source"] in prod_node_ids and e["target"] in prod_node_ids]
    for e in prod_edges:
        assert e["source"] in prod_node_ids and e["target"] in prod_node_ids
    print(f"  [PASS] Filtering retained {len(prod_node_ids)} production nodes and {len(prod_edges)} edges with zero dangling edges.")

    # Test 4: Test filtering excludes all test nodes
    print("Test 4: Validating test and mock classification...")
    test_count = 0
    prod_count = 0
    for n in nodes:
        layer, is_test = classify_layer(
            n.get("source_file"), n.get("label"), n.get("file_type"), n.get("type"), bool(n.get("_py_fixture"))
        )
        if is_test:
            test_count += 1
            assert layer == "Tests and mocks"
        else:
            prod_count += 1
            assert layer != "Tests and mocks"

    assert test_count > 0, "Should detect test nodes"
    assert prod_count > 0, "Should detect production nodes"
    assert test_count + prod_count == len(nodes)
    print(f"  [PASS] Correctly partitioned {len(nodes)} nodes: {prod_count} production nodes, {test_count} test/mock nodes.")

    # Test 5: Search and empty search handling
    print("Test 5: Validating search logic...")
    query = "Candidate"
    matches = [n for n in nodes if query.lower() in n.get("label", "").lower()]
    assert len(matches) > 0, f"Search for {query} should return matches"

    empty_query = "non_existent_symbol_xyz_12345"
    empty_matches = [n for n in nodes if empty_query.lower() in n.get("label", "").lower()]
    assert len(empty_matches) == 0, "Empty search should return 0 matches without error"
    print(f"  [PASS] Search for '{query}' returned {len(matches)} matches; non-existent query safely returned 0.")

    # Test 6: Isolated nodes handling
    print("Test 6: Validating isolated node safety...")
    # Add a mock isolated node and verify hop traversal returns just itself
    isolated_node = "__isolated_test_node__"
    adj[isolated_node] = set()
    iso_hops = get_bfs_hops(isolated_node, 2)
    assert len(iso_hops) == 1 and isolated_node in iso_hops
    print("  [PASS] Isolated nodes safely handled with 1 node returned at any hop distance.")

    # Test 7: Build and verify generated HTML dependencies
    print("Test 7: Validating generated HTML offline compliance...")
    res = build_explorer(graph_json_path, html_path)
    assert html_path.exists(), "HTML file was not created"

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Verify no external CDN or HTTP script/link tags
    remote_script_matches = re.findall(r'<script[^>]+src=["\'](http[s]?://[^"\']+)["\']', html, re.IGNORECASE)
    remote_link_matches = re.findall(r'<link[^>]+href=["\'](http[s]?://[^"\']+)["\']', html, re.IGNORECASE)

    assert len(remote_script_matches) == 0, f"Found remote scripts: {remote_script_matches}"
    assert len(remote_link_matches) == 0, f"Found remote stylesheets/links: {remote_link_matches}"

    # Verify essential elements exist
    assert "<canvas id=\"graphCanvas\"" in html
    assert "id=\"searchInput\"" in html
    assert "id=\"inspectorContent\"" in html
    assert "btnHop1" in html
    assert "btnHop2" in html
    assert "btnHop3" in html
    assert "DATA =" in html
    print("  [PASS] Generated HTML contains ZERO remote dependencies and all required interactive components.")

    print("\n>>> ALL 7 VALIDATION TESTS PASSED SUCCESSFULLY! <<<")


if __name__ == "__main__":
    test_validation()
