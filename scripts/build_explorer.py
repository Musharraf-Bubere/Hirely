#!/usr/bin/env python3
"""
Hirely Enhanced Codebase Explorer Builder
Reads structural data from graphify-out/graph.json and generates a self-contained,
100% offline, responsive, dark-themed interactive HTML explorer at graphify-out/hirely-explorer.html.

Zero external dependencies, zero CDN requests, zero telemetry, zero Gemini API calls.
"""

import json
import os
import sys
from collections import defaultdict
from pathlib import Path


def classify_layer(source_file: str, label: str, file_type: str, node_type: str, is_fixture: bool) -> tuple[str, bool]:
    """
    Classify a node into one of the 9 architectural layers and determine if it is a test/mock.
    Returns (layer_name, is_test).
    """
    sf = (source_file or "").replace("\\", "/")
    lbl = label or ""
    ft = file_type or ""
    ntype = node_type or ""

    # Check for tests, mocks, test fixtures, test rationales
    if (
        sf.startswith("tests/")
        or "/tests/" in sf
        or sf.endswith(".test.js")
        or sf.endswith(".test.jsx")
        or lbl.startswith("test_")
        or lbl.startswith("Fake")
        or lbl.startswith("Mock")
        or is_fixture
        or ft == "rationale"
    ):
        return "Tests and mocks", True

    # External dependencies (third-party packages)
    if ntype == "external" or (not sf and ft != "concept"):
        return "External dependencies", False

    # Frontend
    if sf.startswith("frontend/"):
        return "Frontend", False

    # Backend
    if sf.startswith("backend/"):
        if "app/api/" in sf:
            return "API routes", False
        if "app/services/" in sf:
            return "Business services", False
        if "app/models/" in sf or "app/schemas/" in sf:
            return "Database models and schemas", False
        if "app/ai/" in sf:
            return "AI and RAG", False
        if "app/core/" in sf or "app/db/" in sf or "app/storage/" in sf:
            return "Core infrastructure and storage", False
        if "alembic/" in sf:
            return "Migrations", False
        return "Other/unclassified", False

    return "Other/unclassified", False


def determine_node_type(node: dict, layer: str) -> str:
    """
    Determine accurate node type using actual metadata.
    """
    sf = (node.get("source_file") or "").replace("\\", "/")
    lbl = node.get("label") or ""
    ft = node.get("file_type") or ""
    ntype = node.get("type") or ""

    if ntype == "external" or (not sf and ft != "concept"):
        return "External Library"
    if ft == "concept":
        return "Concept"
    if ft == "rationale":
        return "Rationale"
    if "app/models/" in sf and node.get("_callable_class"):
        return "Database Model"
    if node.get("_callable_class"):
        return "Class"
    if node.get("_callable"):
        return "Function"
    return "Module"


def build_explorer(graph_json_path: Path, output_html_path: Path) -> dict:
    if not graph_json_path.exists():
        raise FileNotFoundError(f"Graph JSON not found at {graph_json_path}")

    print(f"Reading {graph_json_path}...")
    with open(graph_json_path, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    raw_nodes = graph_data.get("nodes", [])
    raw_edges = graph_data.get("links", graph_data.get("edges", []))
    built_commit = graph_data.get("built_at_commit", "unknown")

    print(f"Loaded {len(raw_nodes)} nodes and {len(raw_edges)} edges from commit {built_commit}.")

    node_id_set = {n["id"] for n in raw_nodes if "id" in n}

    # Verify no dangling edges
    valid_edges = []
    dangling_count = 0
    for e in raw_edges:
        s = e.get("source")
        t = e.get("target")
        if s in node_id_set and t in node_id_set:
            valid_edges.append(e)
        else:
            dangling_count += 1

    if dangling_count > 0:
        print(f"Notice: filtered out {dangling_count} edge(s) with nonexistent endpoints.")

    # Calculate in-degree and out-degree
    in_degrees = defaultdict(int)
    out_degrees = defaultdict(int)
    for e in valid_edges:
        out_degrees[e["source"]] += 1
        in_degrees[e["target"]] += 1

    # Enrich nodes with layer and type
    processed_nodes = []
    layer_counts = defaultdict(int)
    community_stats = defaultdict(lambda: {"count": 0, "name": "", "sample": ""})

    for n in raw_nodes:
        nid = n.get("id")
        lbl = n.get("label", nid)
        sf = n.get("source_file", "")
        sl = n.get("source_location", "")
        ft = n.get("file_type", "")
        nt = n.get("type", "")
        is_fix = bool(n.get("_py_fixture"))
        cid = n.get("community", 0)
        cname = n.get("community_name", f"Community {cid}")

        layer, is_test = classify_layer(sf, lbl, ft, nt, is_fix)
        node_kind = determine_node_type(n, layer)

        layer_counts[layer] += 1
        community_stats[cid]["count"] += 1
        community_stats[cid]["name"] = cname
        if not community_stats[cid]["sample"]:
            community_stats[cid]["sample"] = lbl

        processed_nodes.append({
            "id": nid,
            "label": lbl,
            "layer": layer,
            "node_type": node_kind,
            "is_test": is_test,
            "source_file": sf,
            "source_location": sl,
            "community": cid,
            "community_name": cname,
            "in_deg": in_degrees[nid],
            "out_deg": out_degrees[nid],
            "total_deg": in_degrees[nid] + out_degrees[nid],
        })

    # Enrich edges
    processed_edges = []
    relation_counts = defaultdict(int)
    for e in valid_edges:
        rel = e.get("relation", "references")
        relation_counts[rel] += 1
        conf = e.get("confidence", "EXTRACTED")
        is_inferred = (conf == "INFERRED" or e.get("confidence_score", 1.0) < 1.0)

        processed_edges.append({
            "source": e["source"],
            "target": e["target"],
            "relation": rel,
            "is_inferred": is_inferred,
            "context": e.get("context", ""),
        })

    # Prepare layer definitions with consistent modern colors
    layer_colors = {
        "Frontend": "#06b6d4",                         # Cyan / Teal
        "API routes": "#3b82f6",                       # Blue
        "Business services": "#8b5cf6",                # Purple
        "Database models and schemas": "#f59e0b",      # Amber / Gold
        "AI and RAG": "#10b981",                       # Emerald Green
        "Core infrastructure and storage": "#ec4899",  # Pink
        "Migrations": "#f97316",                       # Orange
        "External dependencies": "#64748b",            # Slate
        "Tests and mocks": "#6b7280",                  # Gray
        "Other/unclassified": "#94a3b8",               # Light Slate
    }

    # Relation colors
    relation_colors = {
        "calls": "#3b82f6",
        "imports": "#a855f7",
        "imports_from": "#c084fc",
        "inherits": "#10b981",
        "uses": "#f59e0b",
        "contains": "#64748b",
        "references": "#06b6d4",
        "method": "#14b8a6",
        "rationale_for": "#94a3b8",
        "indirect_call": "#ec4899",
        "re_exports": "#f43f5e",
        "dynamic_import": "#eab308",
    }

    # Communities metadata
    communities_list = []
    for cid, stat in sorted(community_stats.items(), key=lambda x: x[1]["count"], reverse=True):
        communities_list.append({
            "id": cid,
            "name": stat["name"],
            "count": stat["count"],
            "sample": stat["sample"],
        })

    # Package clean JSON bundle
    bundle_data = {
        "built_at_commit": built_commit,
        "nodes": processed_nodes,
        "edges": processed_edges,
        "communities": communities_list,
        "layer_colors": layer_colors,
        "relation_colors": relation_colors,
    }

    print("Generating standalone HTML explorer...")
    html_content = generate_html(bundle_data)

    output_html_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully wrote {output_html_path} ({len(html_content):,} bytes).")

    return {
        "total_nodes": len(processed_nodes),
        "total_edges": len(processed_edges),
        "layer_counts": dict(layer_counts),
        "relation_counts": dict(relation_counts),
        "communities_count": len(communities_list),
        "output_path": str(output_html_path),
    }


def generate_html(bundle: dict) -> str:
    """
    Generates the responsive, dark-themed, 100% offline, standalone HTML file.
    All scripts, styles, and data are strictly inlined with ZERO external network requests.
    """
    json_str = json.dumps(bundle, separators=(",", ":"))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hirely Interactive Codebase Explorer</title>
<style>
  :root {{
    --bg-main: #0a0e17;
    --bg-panel: #111827;
    --bg-card: #1f2937;
    --bg-hover: #374151;
    --border: #1e293b;
    --border-accent: #38bdf8;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent: #38bdf8;
    --accent-glow: rgba(56, 189, 248, 0.35);
    --gold: #f59e0b;
    --radius: 8px;
    --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg-main);
    color: var(--text-primary);
    font-family: var(--font);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  /* Header / Toolbar */
  header {{
    height: 56px;
    background: var(--bg-panel);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    gap: 16px;
    z-index: 10;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: -0.02em;
  }}
  .brand-badge {{
    background: linear-gradient(135deg, #0284c7, #38bdf8);
    color: #fff;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
  }}
  .search-container {{
    position: relative;
    width: 380px;
  }}
  .search-input {{
    width: 100%;
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 8px 12px 8px 32px;
    border-radius: 6px;
    font-size: 13px;
    outline: none;
    transition: all 0.15s ease;
  }}
  .search-input:focus {{
    border-color: var(--border-accent);
    box-shadow: 0 0 0 2px var(--accent-glow);
  }}
  .search-icon {{
    position: absolute;
    left: 10px;
    top: 9px;
    color: var(--text-muted);
    font-size: 14px;
  }}
  .search-dropdown {{
    position: absolute;
    top: 42px;
    left: 0;
    right: 0;
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.5);
    max-height: 380px;
    overflow-y: auto;
    display: none;
    z-index: 100;
  }}
  .search-result-item {{
    padding: 8px 12px;
    cursor: pointer;
    border-bottom: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  .search-result-item:hover, .search-result-item.selected {{
    background: var(--bg-card);
  }}
  .search-result-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .search-result-title {{
    font-weight: 600;
    font-size: 13px;
    color: var(--text-primary);
  }}
  .search-result-badge {{
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 3px;
    font-weight: 600;
  }}
  .search-result-file {{
    font-size: 11px;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }}
  .toolbar-actions {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .btn {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 6px 12px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s ease;
    user-select: none;
  }}
  .btn:hover {{
    background: var(--bg-hover);
    border-color: var(--text-muted);
  }}
  .btn.active {{
    background: #0284c7;
    border-color: #38bdf8;
    color: #fff;
  }}
  .btn-sm {{
    padding: 4px 8px;
    font-size: 11px;
  }}

  /* Main Workspace */
  .workspace {{
    flex: 1;
    display: flex;
    position: relative;
    overflow: hidden;
  }}

  /* Left Filter Drawer */
  .sidebar-left {{
    width: 290px;
    background: var(--bg-panel);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 5;
  }}
  .sidebar-header {{
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .sidebar-scroll {{
    flex: 1;
    overflow-y: auto;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .filter-group {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .filter-group-title {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted);
  }}
  .filter-checkbox {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    cursor: pointer;
    color: var(--text-secondary);
    user-select: none;
    padding: 2px 0;
  }}
  .filter-checkbox:hover {{
    color: var(--text-primary);
  }}
  .filter-checkbox input {{
    appearance: none;
    width: 14px;
    height: 14px;
    border: 1px solid var(--text-muted);
    border-radius: 3px;
    background: var(--bg-main);
    cursor: pointer;
    position: relative;
  }}
  .filter-checkbox input:checked {{
    background: var(--accent);
    border-color: var(--accent);
  }}
  .filter-checkbox input:checked::after {{
    content: '';
    position: absolute;
    left: 4px;
    top: 1px;
    width: 3px;
    height: 7px;
    border: solid #000;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }}
  .dot-indicator {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    display: inline-block;
  }}
  .filter-count {{
    margin-left: auto;
    font-size: 10px;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }}

  /* Graph Canvas Area */
  .canvas-area {{
    flex: 1;
    position: relative;
    background: radial-gradient(circle at center, #0f172a 0%, #0a0e17 100%);
    overflow: hidden;
  }}
  canvas#graphCanvas {{
    width: 100%;
    height: 100%;
    display: block;
    cursor: grab;
  }}
  canvas#graphCanvas:active {{
    cursor: grabbing;
  }}

  /* Floating Floating Bar & Stats overlay */
  .view-controls-bar {{
    position: absolute;
    top: 14px;
    left: 14px;
    background: rgba(17, 24, 39, 0.85);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    z-index: 5;
  }}
  .stats-overlay {{
    position: absolute;
    bottom: 14px;
    left: 14px;
    background: rgba(17, 24, 39, 0.85);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 11px;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 5;
  }}

  /* Right Node Inspector */
  .sidebar-right {{
    width: 340px;
    background: var(--bg-panel);
    border-left: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 5;
  }}
  .inspector-header {{
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .inspector-header h3 {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
  }}
  .inspector-content {{
    flex: 1;
    overflow-y: auto;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .node-title-wrap {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .node-title {{
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    word-break: break-all;
  }}
  .node-badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .badge {{
    font-size: 11px;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 600;
  }}
  .meta-field {{
    display: flex;
    flex-direction: column;
    gap: 3px;
    font-size: 12px;
  }}
  .meta-label {{
    color: var(--text-muted);
    font-size: 10px;
    text-transform: uppercase;
    font-weight: 700;
  }}
  .meta-value {{
    color: var(--text-primary);
    font-family: var(--font-mono);
    font-size: 11px;
    background: var(--bg-card);
    padding: 4px 8px;
    border-radius: 4px;
    word-break: break-all;
  }}
  .connections-section {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .connections-header {{
    font-size: 11px;
    font-weight: 700;
    color: var(--text-secondary);
    display: flex;
    justify-content: space-between;
  }}
  .connections-list {{
    max-height: 180px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  .conn-item {{
    padding: 5px 8px;
    background: var(--bg-card);
    border-radius: 4px;
    font-size: 11px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-left: 3px solid transparent;
    transition: background 0.15s ease;
  }}
  .conn-item:hover {{
    background: var(--bg-hover);
  }}
  .conn-label {{
    font-weight: 600;
    color: var(--text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 190px;
  }}
  .conn-rel {{
    font-size: 10px;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }}

  /* Breadcrumbs */
  .breadcrumbs {{
    display: flex;
    align-items: center;
    gap: 4px;
    overflow-x: auto;
    font-size: 11px;
    padding-bottom: 4px;
  }}
  .crumb {{
    cursor: pointer;
    color: var(--accent);
    white-space: nowrap;
  }}
  .crumb:hover {{
    text-decoration: underline;
  }}

  /* Tooltip overlay */
  .graph-tooltip {{
    position: absolute;
    background: rgba(17, 24, 39, 0.95);
    border: 1px solid var(--border-accent);
    color: var(--text-primary);
    padding: 8px 12px;
    border-radius: 5px;
    font-size: 12px;
    pointer-events: none;
    box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    z-index: 1000;
    display: none;
    max-width: 320px;
  }}
  .graph-tooltip b {{
    display: block;
    color: var(--accent);
    margin-bottom: 2px;
  }}

  /* Help Modal */
  .modal-backdrop {{
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.75);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 2000;
  }}
  .modal-box {{
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    width: 580px;
    max-width: 90vw;
    max-height: 85vh;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .modal-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .modal-header h2 {{
    font-size: 18px;
  }}
</style>
</head>
<body>

<header>
  <div class="brand">
    <span>Hirely Explorer</span>
    <span class="brand-badge">Graphify</span>
  </div>

  <div class="search-container">
    <span class="search-icon">🔍</span>
    <input id="searchInput" class="search-input" type="text" placeholder="Search symbol, class, function, or file..." autocomplete="off">
    <div id="searchDropdown" class="search-dropdown"></div>
  </div>

  <div class="toolbar-actions">
    <div style="display: flex; align-items: center; gap: 4px; margin-right: 6px;">
      <span style="font-size: 11px; color: var(--text-muted); font-weight: 600;">HOPS:</span>
      <button class="btn btn-sm" id="btnHop1" onclick="setHopDepth(1)">1</button>
      <button class="btn btn-sm active" id="btnHop2" onclick="setHopDepth(2)">2</button>
      <button class="btn btn-sm" id="btnHop3" onclick="setHopDepth(3)">3</button>
    </div>

    <div style="display: flex; align-items: center; gap: 4px; margin-right: 6px;">
      <button class="btn btn-sm active" id="btnLayoutOrganic" onclick="setLayout('organic')">Organic</button>
      <button class="btn btn-sm" id="btnLayoutHierarchical" onclick="setLayout('hierarchical')">Hierarchical</button>
      <button class="btn btn-sm" id="btnLayoutConcentric" onclick="setLayout('concentric')">Concentric</button>
    </div>

    <button class="btn btn-sm" id="btnToggleTests" onclick="toggleTests()">Hide Tests</button>
    <button class="btn btn-sm" onclick="resetToOverview()">Overview</button>
    <button class="btn btn-sm" onclick="fitView()">Fit</button>
    <button class="btn btn-sm" onclick="toggleHelp()">Help</button>
  </div>
</header>

<div class="workspace">
  <!-- Left Sidebar (Filters) -->
  <aside class="sidebar-left">
    <div class="sidebar-header">
      <span>Architectural Filters</span>
      <button class="btn btn-sm" onclick="toggleAllLayers()">Toggle</button>
    </div>
    <div class="sidebar-scroll">
      <div class="filter-group">
        <span class="filter-group-title">Layers</span>
        <div id="layerFilters"></div>
      </div>

      <div class="filter-group">
        <span class="filter-group-title">Relationship Types</span>
        <div id="relationFilters"></div>
      </div>

      <div class="filter-group">
        <span class="filter-group-title">Community Pruning</span>
        <label style="font-size: 11px; color: var(--text-secondary); display: flex; flex-direction: column; gap: 4px;">
          <span>Min Community Size: <b id="minCommVal">1</b></span>
          <input type="range" id="minCommRange" min="1" max="25" value="1" oninput="updateMinComm(this.value)" style="width: 100%;">
        </label>
      </div>
    </div>
  </aside>

  <!-- Central Canvas -->
  <main class="canvas-area">
    <div class="view-controls-bar">
      <span id="activeModeLabel" style="font-weight: 600; color: var(--accent);">Architecture Overview</span>
      <span style="color: var(--border);">|</span>
      <label style="display: flex; align-items: center; gap: 4px; font-size: 11px; cursor: pointer;">
        <input type="checkbox" id="cbShowLabels" checked onchange="toggleLabels(this.checked)"> Labels
      </label>
      <label style="display: flex; align-items: center; gap: 4px; font-size: 11px; cursor: pointer;">
        <input type="checkbox" id="cbShowInferred" checked onchange="toggleInferred(this.checked)"> Inferred (Dashed)
      </label>
    </div>

    <canvas id="graphCanvas"></canvas>

    <div class="stats-overlay">
      <span id="statVisibleNodes">Visible: 0 nodes</span>
      <span>&bull;</span>
      <span id="statVisibleEdges">0 edges</span>
      <span>&bull;</span>
      <span id="statFilteredNodes">0 filtered</span>
    </div>

    <div id="graphTooltip" class="graph-tooltip"></div>
  </main>

  <!-- Right Sidebar (Inspector) -->
  <aside class="sidebar-right">
    <div class="inspector-header">
      <h3>Node Inspector</h3>
      <button class="btn btn-sm" id="btnBackHistory" onclick="navigateBack()" style="display:none;">&larr; Back</button>
    </div>
    <div class="inspector-content" id="inspectorContent">
      <div style="color: var(--text-muted); font-size: 13px; font-style: italic; text-align: center; margin-top: 40px;">
        Click any node in the graph or search above to inspect relationships.
      </div>
    </div>
  </aside>
</div>

<!-- Help Modal -->
<div id="helpModal" class="modal-backdrop" onclick="toggleHelp()">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h2>Hirely Graph Explorer Guide</h2>
      <button class="btn btn-sm" onclick="toggleHelp()">&times;</button>
    </div>
    <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.6; display: flex; flex-direction: column; gap: 12px;">
      <p><b>Focus Mode:</b> Click any node or pick from the search box to view its immediate neighborhood. Toggle <b>1, 2, or 3 hops</b> to see caller/callee chains.</p>
      <p><b>Overview Mode:</b> When no node is focused, the explorer displays primary architectural hubs and classes, avoiding the 2,000-node hairball.</p>
      <p><b>Visual Cues:</b>
        <br>&bull; <b>Solid Arrows:</b> Explicit AST extracted dependencies.
        <br>&bull; <b>Dashed Arrows:</b> Inferred semantic relationships (clearly distinguished).
        <br>&bull; <b>Gold Glow:</b> The currently focused root node.
      </p>
      <p><b>Hotkeys:</b>
        <br>&bull; <kbd>Escape</kbd>: Clear focus / return to Overview.
        <br>&bull; <kbd>1, 2, 3</kbd>: Set hop depth.
        <br>&bull; <kbd>T</kbd>: Toggle Test/Mock nodes.
      </p>
    </div>
  </div>
</div>

<script>
// RAW DATA BUNDLE
const DATA = {json_str};

// STATE
const STATE = {{
  focusNodeId: null,
  hopDepth: 2,
  layout: 'organic',
  hideTests: true,
  showLabels: true,
  showInferred: true,
  minCommunitySize: 1,
  activeLayers: new Set(Object.keys(DATA.layer_colors)),
  activeRelations: new Set(Object.keys(DATA.relation_colors)),
  history: [],
  scale: 1,
  panX: 0,
  panY: 0,
}};

// Initialize layer filters default: hide tests
STATE.activeLayers.delete('Tests and mocks');

// Fast Lookup Structures
const nodeMap = new Map();
DATA.nodes.forEach(n => nodeMap.set(n.id, n));

const outgoingMap = new Map();
const incomingMap = new Map();
DATA.nodes.forEach(n => {{
  outgoingMap.set(n.id, []);
  incomingMap.set(n.id, []);
}});

DATA.edges.forEach(e => {{
  if (outgoingMap.has(e.source)) outgoingMap.get(e.source).push(e);
  if (incomingMap.has(e.target)) incomingMap.get(e.target).push(e);
}});

// Computed Subgraph
let visibleNodes = [];
let visibleEdges = [];
let nodePos = new Map();
let nodeVel = new Map();
let simRunning = false;
let simTicks = 0;

// Canvas setup
const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');
let width = canvas.clientWidth;
let height = canvas.clientHeight;

function resizeCanvas() {{
  const dpr = window.devicePixelRatio || 1;
  width = canvas.clientWidth;
  height = canvas.clientHeight;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  ctx.scale(dpr, dpr);
  render();
}}
window.addEventListener('resize', resizeCanvas);

// LAYER FILTERS UI
function setupFilterUI() {{
  const layerContainer = document.getElementById('layerFilters');
  layerContainer.innerHTML = '';
  Object.keys(DATA.layer_colors).forEach(layer => {{
    const count = DATA.nodes.filter(n => n.layer === layer).length;
    const color = DATA.layer_colors[layer];
    const isChecked = STATE.activeLayers.has(layer);

    const lbl = document.createElement('label');
    lbl.className = 'filter-checkbox';
    lbl.innerHTML = `
      <input type="checkbox" ${{isChecked ? 'checked' : ''}} data-layer="${{layer}}">
      <span class="dot-indicator" style="background:${{color}}"></span>
      <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:170px;">${{layer}}</span>
      <span class="filter-count">${{count}}</span>
    `;
    lbl.querySelector('input').addEventListener('change', (e) => {{
      if (e.target.checked) STATE.activeLayers.add(layer);
      else STATE.activeLayers.delete(layer);
      recomputeGraph();
    }});
    layerContainer.appendChild(lbl);
  }});

  const relContainer = document.getElementById('relationFilters');
  relContainer.innerHTML = '';
  Object.keys(DATA.relation_colors).forEach(rel => {{
    const count = DATA.edges.filter(e => e.relation === rel).length;
    const color = DATA.relation_colors[rel];
    const isChecked = STATE.activeRelations.has(rel);

    const lbl = document.createElement('label');
    lbl.className = 'filter-checkbox';
    lbl.innerHTML = `
      <input type="checkbox" ${{isChecked ? 'checked' : ''}} data-rel="${{rel}}">
      <span class="dot-indicator" style="background:${{color}}"></span>
      <span style="font-family:var(--font-mono); font-size:11px;">${{rel}}</span>
      <span class="filter-count">${{count}}</span>
    `;
    lbl.querySelector('input').addEventListener('change', (e) => {{
      if (e.target.checked) STATE.activeRelations.add(rel);
      else STATE.activeRelations.delete(rel);
      recomputeGraph();
    }});
    relContainer.appendChild(lbl);
  }});
}}

// GRAPH COMPUTATION: BFS HOPS OR OVERVIEW
function recomputeGraph() {{
  const communityCounts = new Map();
  DATA.communities.forEach(c => communityCounts.set(c.id, c.count));

  function isNodeAllowed(n) {{
    if (STATE.hideTests && n.is_test) return false;
    if (!STATE.activeLayers.has(n.layer)) return false;
    if (communityCounts.get(n.community) < STATE.minCommunitySize) return false;
    return true;
  }}

  if (STATE.focusNodeId && nodeMap.has(STATE.focusNodeId)) {{
    // FOCUS MODE: BFS Neighborhood
    const visited = new Map(); // id -> hop distance
    const queue = [{{ id: STATE.focusNodeId, dist: 0 }}];
    visited.set(STATE.focusNodeId, 0);

    while (queue.length > 0) {{
      const {{ id, dist }} = queue.shift();
      if (dist >= STATE.hopDepth) continue;

      // Check outgoing
      (outgoingMap.get(id) || []).forEach(e => {{
        if (!STATE.activeRelations.has(e.relation)) return;
        if (!STATE.showInferred && e.is_inferred) return;
        const targetNode = nodeMap.get(e.target);
        if (targetNode && isNodeAllowed(targetNode) && !visited.has(e.target)) {{
          visited.set(e.target, dist + 1);
          queue.push({{ id: e.target, dist: dist + 1 }});
        }}
      }});

      // Check incoming
      (incomingMap.get(id) || []).forEach(e => {{
        if (!STATE.activeRelations.has(e.relation)) return;
        if (!STATE.showInferred && e.is_inferred) return;
        const sourceNode = nodeMap.get(e.source);
        if (sourceNode && isNodeAllowed(sourceNode) && !visited.has(e.source)) {{
          visited.set(e.source, dist + 1);
          queue.push({{ id: e.source, dist: dist + 1 }});
        }}
      }});
    }}

    visibleNodes = Array.from(visited.keys()).map(id => {{
      const n = {{ ...nodeMap.get(id) }};
      n.hopDist = visited.get(id);
      return n;
    }});

    document.getElementById('activeModeLabel').innerHTML = `Focus: <span style="color:#fff;">${{nodeMap.get(STATE.focusNodeId).label}}</span> (${{STATE.hopDepth}} hops)`;
  }} else {{
    // OVERVIEW MODE: Show primary architectural classes, routes, models, and services
    visibleNodes = DATA.nodes.filter(n => {{
      if (!isNodeAllowed(n)) return false;
      // In overview mode, emphasize classes, models, routes, or nodes with degree >= 4
      return (
        n.node_type === 'Database Model' ||
        n.node_type === 'Class' ||
        n.layer === 'API routes' ||
        n.layer === 'Business services' ||
        n.total_deg >= 4
      );
    }}).slice(0, 160); // Cap overview to 160 hubs for buttery smooth display

    document.getElementById('activeModeLabel').textContent = 'Architecture Overview (Core Hubs)';
  }}

  // Filter edges between visible nodes
  const visibleNodeSet = new Set(visibleNodes.map(n => n.id));
  visibleEdges = DATA.edges.filter(e => {{
    if (!visibleNodeSet.has(e.source) || !visibleNodeSet.has(e.target)) return false;
    if (!STATE.activeRelations.has(e.relation)) return false;
    if (!STATE.showInferred && e.is_inferred) return false;
    return true;
  }});

  // Update stats
  document.getElementById('statVisibleNodes').textContent = `Visible: ${{visibleNodes.length}} nodes`;
  document.getElementById('statVisibleEdges').textContent = `${{visibleEdges.length}} edges`;
  document.getElementById('statFilteredNodes').textContent = `${{DATA.nodes.length - visibleNodes.length}} filtered out`;

  initLayoutPositions();
}}

// LAYOUT ENGINES
function initLayoutPositions() {{
  const centerX = width / 2;
  const centerY = height / 2;

  if (STATE.layout === 'concentric' && STATE.focusNodeId) {{
    // Concentric layout around focus node
    const ringRadius = [0, 140, 280, 420];
    const hopGroups = [[], [], [], []];
    visibleNodes.forEach(n => {{
      const h = n.hopDist !== undefined ? Math.min(n.hopDist, 3) : 1;
      hopGroups[h].push(n);
    }});

    hopGroups.forEach((group, hop) => {{
      const r = ringRadius[hop];
      const count = group.length;
      group.forEach((n, idx) => {{
        if (hop === 0) {{
          nodePos.set(n.id, {{ x: centerX, y: centerY }});
        }} else {{
          const angle = (idx / count) * 2 * Math.PI;
          nodePos.set(n.id, {{
            x: centerX + r * Math.cos(angle),
            y: centerY + r * Math.sin(angle),
          }});
        }}
      }});
    }});
    simRunning = false;
    fitView();
    render();
    return;
  }}

  if (STATE.layout === 'hierarchical') {{
    // Tiered DAG ranking based on Architectural Layer
    const layerRank = {{
      'External dependencies': 0,
      'Frontend': 1,
      'API routes': 2,
      'Business services': 3,
      'AI and RAG': 4,
      'Database models and schemas': 5,
      'Core infrastructure and storage': 6,
      'Migrations': 7,
      'Tests and mocks': 8,
      'Other/unclassified': 9,
    }};

    const rankBuckets = Array.from({{ length: 10 }}, () => []);
    visibleNodes.forEach(n => {{
      const r = layerRank[n.layer] !== undefined ? layerRank[n.layer] : 9;
      rankBuckets[r].push(n);
    }});

    const tierHeight = 110;
    const startY = centerY - (4 * tierHeight);

    rankBuckets.forEach((bucket, rank) => {{
      const y = startY + (rank * tierHeight);
      const count = bucket.length;
      const spacing = Math.min(130, (width * 0.85) / Math.max(count, 1));
      const startX = centerX - ((count - 1) * spacing) / 2;

      bucket.forEach((n, idx) => {{
        nodePos.set(n.id, {{
          x: startX + idx * spacing,
          y: y,
        }});
      }});
    }});
    simRunning = false;
    fitView();
    render();
    return;
  }}

  // Organic Physics Simulation (ForceAtlas2 / Coulomb-Hooke)
  visibleNodes.forEach(n => {{
    if (!nodePos.has(n.id)) {{
      nodePos.set(n.id, {{
        x: centerX + (Math.random() - 0.5) * 400,
        y: centerY + (Math.random() - 0.5) * 400,
      }});
    }}
    nodeVel.set(n.id, {{ vx: 0, vy: 0 }});
  }});

  simTicks = 0;
  simRunning = true;
  requestAnimationFrame(physicsStep);
}}

function physicsStep() {{
  if (!simRunning) return;
  simTicks++;

  const nodes = visibleNodes;
  const kRepulse = 1800;
  const kAttract = 0.04;
  const l0 = 90;
  const damping = 0.85;

  // Repulsion between nodes
  for (let i = 0; i < nodes.length; i++) {{
    const p1 = nodePos.get(nodes[i].id);
    const v1 = nodeVel.get(nodes[i].id);
    for (let j = i + 1; j < nodes.length; j++) {{
      const p2 = nodePos.get(nodes[j].id);
      const v2 = nodeVel.get(nodes[j].id);
      let dx = p1.x - p2.x;
      let dy = p1.y - p2.y;
      let d2 = dx * dx + dy * dy;
      if (d2 < 1) {{ dx = Math.random() * 2; dy = Math.random() * 2; d2 = 1; }}
      const dist = Math.sqrt(d2);
      const force = kRepulse / d2;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;

      v1.vx += fx; v1.vy += fy;
      v2.vx -= fx; v2.vy -= fy;
    }}
  }}

  // Attraction along edges
  visibleEdges.forEach(e => {{
    const p1 = nodePos.get(e.source);
    const p2 = nodePos.get(e.target);
    if (!p1 || !p2) return;
    const v1 = nodeVel.get(e.source);
    const v2 = nodeVel.get(e.target);

    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const force = (dist - l0) * kAttract;
    const fx = (dx / dist) * force;
    const fy = (dy / dist) * force;

    v1.vx += fx; v1.vy += fy;
    v2.vx -= fx; v2.vy -= fy;
  }});

  // Center gravity
  const cx = width / 2;
  const cy = height / 2;
  nodes.forEach(n => {{
    const p = nodePos.get(n.id);
    const v = nodeVel.get(n.id);
    v.vx += (cx - p.x) * 0.002;
    v.vy += (cy - p.y) * 0.002;

    p.x += v.vx;
    p.y += v.vy;
    v.vx *= damping;
    v.vy *= damping;
  }});

  render();

  if (simTicks < 180) {{
    requestAnimationFrame(physicsStep);
  }} else {{
    simRunning = false;
    render();
  }}
}}

// RENDERING
let hoveredNode = null;
let draggingNode = null;
let isPanning = false;
let lastMouseX = 0;
let lastMouseY = 0;

function render() {{
  ctx.save();
  ctx.clearRect(0, 0, width, height);

  // Apply camera pan & zoom
  ctx.translate(STATE.panX, STATE.panY);
  ctx.scale(STATE.scale, STATE.scale);

  // 1. Draw Edges
  visibleEdges.forEach(e => {{
    const p1 = nodePos.get(e.source);
    const p2 = nodePos.get(e.target);
    if (!p1 || !p2) return;

    const isConnectedToHover = hoveredNode && (e.source === hoveredNode.id || e.target === hoveredNode.id);
    const isConnectedToFocus = STATE.focusNodeId && (e.source === STATE.focusNodeId || e.target === STATE.focusNodeId);

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);

    const edgeColor = DATA.relation_colors[e.relation] || '#64748b';
    ctx.strokeStyle = edgeColor;

    if (e.is_inferred) {{
      ctx.setLineDash([4, 4]); // Dashed line for inferred relationships
    }}

    if (isConnectedToHover || isConnectedToFocus) {{
      ctx.globalAlpha = 0.95;
      ctx.lineWidth = 2.4;
    }} else {{
      ctx.globalAlpha = STATE.focusNodeId ? 0.35 : 0.45;
      ctx.lineWidth = 1.0;
    }}
    ctx.stroke();

    // Draw directed arrow
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    const angle = Math.atan2(dy, dx);
    const nodeR = 14;
    const arrowX = p2.x - nodeR * Math.cos(angle);
    const arrowY = p2.y - nodeR * Math.sin(angle);
    const arrowSize = 6;

    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.moveTo(arrowX, arrowY);
    ctx.lineTo(arrowX - arrowSize * Math.cos(angle - Math.PI / 6), arrowY - arrowSize * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(arrowX - arrowSize * Math.cos(angle + Math.PI / 6), arrowY - arrowSize * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fillStyle = edgeColor;
    ctx.fill();
    ctx.restore();
  }});

  // 2. Draw Nodes
  visibleNodes.forEach(n => {{
    const p = nodePos.get(n.id);
    if (!p) return;

    const isFocused = n.id === STATE.focusNodeId;
    const isHovered = hoveredNode && n.id === hoveredNode.id;
    const nodeColor = DATA.layer_colors[n.layer] || '#94a3b8';

    ctx.save();

    // Focus / Hover Glow Halo
    if (isFocused) {{
      ctx.beginPath();
      ctx.arc(p.x, p.y, 24, 0, 2 * Math.PI);
      ctx.fillStyle = 'rgba(245, 158, 11, 0.25)';
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = '#f59e0b';
      ctx.stroke();
    }} else if (isHovered) {{
      ctx.beginPath();
      ctx.arc(p.x, p.y, 20, 0, 2 * Math.PI);
      ctx.fillStyle = 'rgba(56, 189, 248, 0.25)';
      ctx.fill();
    }}

    // Draw node shape based on node_type
    const r = Math.max(10, Math.min(22, 10 + Math.log2(n.total_deg + 1) * 2.5));

    if (n.node_type === 'Database Model') {{
      // Cylinder / Database representation
      ctx.beginPath();
      ctx.rect(p.x - r, p.y - r * 0.8, r * 2, r * 1.6);
      ctx.fillStyle = '#1e293b';
      ctx.fill();
      ctx.lineWidth = isFocused ? 2.5 : 1.8;
      ctx.strokeStyle = '#f59e0b'; // Gold border for database models
      ctx.stroke();
    }} else if (n.node_type === 'Class') {{
      // Rounded Rectangle for Classes
      ctx.beginPath();
      ctx.roundRect(p.x - r, p.y - r, r * 2, r * 2, 5);
      ctx.fillStyle = '#1e293b';
      ctx.fill();
      ctx.lineWidth = isFocused ? 2.5 : 1.8;
      ctx.strokeStyle = nodeColor;
      ctx.stroke();
    }} else if (n.node_type === 'External Library') {{
      // Dashed slate box for external modules
      ctx.beginPath();
      ctx.roundRect(p.x - r, p.y - r, r * 2, r * 2, 4);
      ctx.setLineDash([3, 3]);
      ctx.fillStyle = '#111827';
      ctx.fill();
      ctx.lineWidth = 1.4;
      ctx.strokeStyle = '#94a3b8';
      ctx.stroke();
    }} else {{
      // Circle for functions & others
      ctx.beginPath();
      ctx.arc(p.x, p.y, r, 0, 2 * Math.PI);
      ctx.fillStyle = '#1e293b';
      ctx.fill();
      ctx.lineWidth = isFocused ? 2.5 : 1.5;
      ctx.strokeStyle = nodeColor;
      ctx.stroke();
    }}

    // Node Type Icon / Text Badge
    ctx.setLineDash([]);
    ctx.fillStyle = nodeColor;
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    let badgeText = 'fn';
    if (n.node_type === 'Database Model') badgeText = 'DB';
    else if (n.node_type === 'Class') badgeText = 'C';
    else if (n.node_type === 'External Library') badgeText = 'ext';
    else if (n.layer === 'Frontend') badgeText = 'UI';
    ctx.fillText(badgeText, p.x, p.y);

    // Node Label
    if (STATE.showLabels || isFocused || isHovered || n.total_deg >= 15) {{
      ctx.fillStyle = isFocused ? '#f59e0b' : (isHovered ? '#38bdf8' : '#e2e8f0');
      ctx.font = isFocused ? 'bold 12px sans-serif' : '11px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      ctx.fillText(n.label, p.x, p.y + r + 4);
    }}

    ctx.restore();
  }});

  ctx.restore();
}}

// CAMERA / VIEW CONTROLS
function fitView() {{
  if (visibleNodes.length === 0) return;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  visibleNodes.forEach(n => {{
    const p = nodePos.get(n.id);
    if (!p) return;
    minX = Math.min(minX, p.x);
    maxX = Math.max(maxX, p.x);
    minY = Math.min(minY, p.y);
    maxY = Math.max(maxY, p.y);
  }});

  const boxW = Math.max(maxX - minX + 160, 200);
  const boxH = Math.max(maxY - minY + 160, 200);

  STATE.scale = Math.min(1.6, Math.max(0.25, Math.min(width / boxW, height / boxH)));
  STATE.panX = width / 2 - ((minX + maxX) / 2) * STATE.scale;
  STATE.panY = height / 2 - ((minY + maxY) / 2) * STATE.scale;
  render();
}}

// INTERACTION: MOUSE & TOUCH
function screenToWorld(sx, sy) {{
  return {{
    x: (sx - STATE.panX) / STATE.scale,
    y: (sy - STATE.panY) / STATE.scale,
  }};
}}

function findNodeAt(sx, sy) {{
  const w = screenToWorld(sx, sy);
  for (let i = visibleNodes.length - 1; i >= 0; i--) {{
    const n = visibleNodes[i];
    const p = nodePos.get(n.id);
    if (!p) continue;
    const dx = w.x - p.x;
    const dy = w.y - p.y;
    const r = Math.max(16, 12 + Math.log2(n.total_deg + 1) * 2.5);
    if (dx * dx + dy * dy <= r * r) return n;
  }}
  return null;
}}

canvas.addEventListener('mousedown', e => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const hit = findNodeAt(mx, my);

  if (hit) {{
    draggingNode = hit;
    selectNode(hit.id);
  }} else {{
    isPanning = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  }}
}});

window.addEventListener('mousemove', e => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  if (isPanning) {{
    STATE.panX += e.clientX - lastMouseX;
    STATE.panY += e.clientY - lastMouseY;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
    render();
    return;
  }}

  if (draggingNode) {{
    const w = screenToWorld(mx, my);
    const p = nodePos.get(draggingNode.id);
    if (p) {{ p.x = w.x; p.y = w.y; }}
    render();
    return;
  }}

  // Hover detection
  const hit = findNodeAt(mx, my);
  const tooltip = document.getElementById('graphTooltip');

  if (hit) {{
    canvas.style.cursor = 'pointer';
    hoveredNode = hit;
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 14) + 'px';
    tooltip.style.top = (e.clientY + 14) + 'px';
    tooltip.innerHTML = `
      <b>${{hit.label}}</b>
      <div style="font-size:11px; color:#94a3b8;">${{hit.layer}} &bull; ${{hit.node_type}}</div>
      <div style="font-size:10px; font-family:var(--font-mono); color:#cbd5e1; margin-top:3px;">${{hit.source_file || 'external'}}</div>
      <div style="font-size:10px; color:#38bdf8; margin-top:2px;">Degree: ${{hit.total_deg}} (${{hit.in_deg}} in, ${{hit.out_deg}} out)</div>
    `;
    render();
  }} else if (hoveredNode) {{
    canvas.style.cursor = 'grab';
    hoveredNode = null;
    tooltip.style.display = 'none';
    render();
  }}
}});

window.addEventListener('mouseup', () => {{
  isPanning = false;
  draggingNode = null;
}});

canvas.addEventListener('wheel', e => {{
  e.preventDefault();
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;

  const wBefore = screenToWorld(mx, my);
  STATE.scale = Math.min(4.0, Math.max(0.15, STATE.scale * zoomFactor));
  STATE.panX = mx - wBefore.x * STATE.scale;
  STATE.panY = my - wBefore.y * STATE.scale;
  render();
}}, {{ passive: false }});

canvas.addEventListener('dblclick', e => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const hit = findNodeAt(mx, my);
  if (hit) {{
    setFocusNode(hit.id);
  }}
}});

// INSPECTOR & SELECTION
function selectNode(id) {{
  if (!nodeMap.has(id)) return;
  const node = nodeMap.get(id);

  if (STATE.history.length === 0 || STATE.history[STATE.history.length - 1] !== id) {{
    STATE.history.push(id);
  }}
  document.getElementById('btnBackHistory').style.display = STATE.history.length > 1 ? 'inline-flex' : 'none';

  const inConns = incomingMap.get(id) || [];
  const outConns = outgoingMap.get(id) || [];

  const inHtml = inConns.map(e => {{
    const s = nodeMap.get(e.source);
    if (!s) return '';
    const color = DATA.relation_colors[e.relation] || '#64748b';
    return `
      <div class="conn-item" style="border-left-color:${{color}};" onclick="setFocusNode('${{s.id}}')">
        <span class="conn-label">${{s.label}}</span>
        <span class="conn-rel">${{e.relation}}${{e.is_inferred ? ' [inf]' : ''}}</span>
      </div>
    `;
  }}).join('') || '<div style="color:var(--text-muted); font-size:11px;">None</div>';

  const outHtml = outConns.map(e => {{
    const t = nodeMap.get(e.target);
    if (!t) return '';
    const color = DATA.relation_colors[e.relation] || '#64748b';
    return `
      <div class="conn-item" style="border-left-color:${{color}};" onclick="setFocusNode('${{t.id}}')">
        <span class="conn-label">${{t.label}}</span>
        <span class="conn-rel">${{e.relation}}${{e.is_inferred ? ' [inf]' : ''}}</span>
      </div>
    `;
  }}).join('') || '<div style="color:var(--text-muted); font-size:11px;">None</div>';

  const layerColor = DATA.layer_colors[node.layer] || '#94a3b8';

  document.getElementById('inspectorContent').innerHTML = `
    <div class="node-title-wrap">
      <div class="node-title">${{node.label}}</div>
      <div class="node-badges">
        <span class="badge" style="background:${{layerColor}}33; color:${{layerColor}}; border:1px solid ${{layerColor}};">${{node.layer}}</span>
        <span class="badge" style="background:#1e293b; color:#cbd5e1; border:1px solid #475569;">${{node.node_type}}</span>
        <span class="badge" style="background:#1e293b; color:#94a3b8;">${{node.community_name}}</span>
      </div>
    </div>

    <div style="display:flex; gap:6px;">
      <button class="btn btn-sm" style="flex:1; justify-content:center; background:#0284c7; border-color:#38bdf8;" onclick="setFocusNode('${{node.id}}')">Focus Neighborhood</button>
      <button class="btn btn-sm" onclick="centerOnNode('${{node.id}}')">Center</button>
    </div>

    <div class="meta-field">
      <span class="meta-label">Source Path</span>
      <span class="meta-value">${{node.source_file || 'external package'}}${{node.source_location ? ':' + node.source_location : ''}}</span>
    </div>

    <div class="meta-field">
      <span class="meta-label">Connections</span>
      <div style="display:flex; gap:12px; font-size:12px; margin-top:2px;">
        <span>Incoming (Callers): <b>${{node.in_deg}}</b></span>
        <span>Outgoing (Callees): <b>${{node.out_deg}}</b></span>
      </div>
    </div>

    <div class="connections-section">
      <div class="connections-header">
        <span>Incoming Callers (${{inConns.length}})</span>
      </div>
      <div class="connections-list">${{inHtml}}</div>
    </div>

    <div class="connections-section">
      <div class="connections-header">
        <span>Outgoing Dependencies (${{outConns.length}})</span>
      </div>
      <div class="connections-list">${{outHtml}}</div>
    </div>
  `;

  render();
}}

function setFocusNode(id) {{
  STATE.focusNodeId = id;
  recomputeGraph();
  selectNode(id);
}}

function centerOnNode(id) {{
  const p = nodePos.get(id);
  if (!p) return;
  STATE.panX = width / 2 - p.x * STATE.scale;
  STATE.panY = height / 2 - p.y * STATE.scale;
  render();
}}

function resetToOverview() {{
  STATE.focusNodeId = null;
  recomputeGraph();
  fitView();
  document.getElementById('inspectorContent').innerHTML = `
    <div style="color: var(--text-muted); font-size: 13px; font-style: italic; text-align: center; margin-top: 40px;">
      Overview mode active. Select any symbol to inspect connections.
    </div>
  `;
}}

function navigateBack() {{
  if (STATE.history.length > 1) {{
    STATE.history.pop(); // remove current
    const prev = STATE.history[STATE.history.length - 1];
    setFocusNode(prev);
  }}
}}

// TOOLBAR ACTIONS
function setHopDepth(h) {{
  STATE.hopDepth = h;
  ['1', '2', '3'].forEach(d => {{
    document.getElementById('btnHop' + d).classList.toggle('active', d === String(h));
  }});
  recomputeGraph();
}}

function setLayout(layoutName) {{
  STATE.layout = layoutName;
  ['Organic', 'Hierarchical', 'Concentric'].forEach(l => {{
    document.getElementById('btnLayout' + l).classList.toggle('active', l.toLowerCase() === layoutName);
  }});
  initLayoutPositions();
}}

function toggleTests() {{
  STATE.hideTests = !STATE.hideTests;
  const btn = document.getElementById('btnToggleTests');
  btn.textContent = STATE.hideTests ? 'Show Tests' : 'Hide Tests';
  btn.classList.toggle('active', !STATE.hideTests);

  const testCheckbox = document.querySelector('input[data-layer="Tests and mocks"]');
  if (testCheckbox) testCheckbox.checked = !STATE.hideTests;

  if (STATE.hideTests) STATE.activeLayers.delete('Tests and mocks');
  else STATE.activeLayers.add('Tests and mocks');

  recomputeGraph();
}}

function toggleAllLayers() {{
  const allActive = STATE.activeLayers.size === Object.keys(DATA.layer_colors).length;
  document.querySelectorAll('#layerFilters input').forEach(cb => {{
    cb.checked = !allActive;
  }});
  if (allActive) STATE.activeLayers.clear();
  else Object.keys(DATA.layer_colors).forEach(l => STATE.activeLayers.add(l));
  recomputeGraph();
}}

function toggleLabels(checked) {{
  STATE.showLabels = checked;
  render();
}}

function toggleInferred(checked) {{
  STATE.showInferred = checked;
  recomputeGraph();
}}

function updateMinComm(val) {{
  STATE.minCommunitySize = parseInt(val, 10);
  document.getElementById('minCommVal').textContent = val;
  recomputeGraph();
}}

function toggleHelp() {{
  const m = document.getElementById('helpModal');
  m.style.display = m.style.display === 'flex' ? 'none' : 'flex';
}}

// SEARCH SYSTEM
const searchInput = document.getElementById('searchInput');
const searchDropdown = document.getElementById('searchDropdown');

searchInput.addEventListener('input', () => {{
  const q = searchInput.value.toLowerCase().trim();
  if (!q) {{
    searchDropdown.style.display = 'none';
    return;
  }}

  const matches = DATA.nodes.filter(n => {{
    return n.label.toLowerCase().includes(q) || (n.source_file && n.source_file.toLowerCase().includes(q));
  }}).slice(0, 16);

  if (matches.length === 0) {{
    searchDropdown.innerHTML = '<div style="padding:10px; font-size:12px; color:var(--text-muted);">No matching symbols found.</div>';
    searchDropdown.style.display = 'block';
    return;
  }}

  searchDropdown.innerHTML = matches.map(m => {{
    const layerColor = DATA.layer_colors[m.layer] || '#94a3b8';
    return `
      <div class="search-result-item" onclick="pickSearch('${{m.id}}')">
        <div class="search-result-top">
          <span class="search-result-title">${{m.label}}</span>
          <span class="search-result-badge" style="background:${{layerColor}}33; color:${{layerColor}};">${{m.layer}}</span>
        </div>
        <span class="search-result-file">${{m.source_file || 'external'}}</span>
      </div>
    `;
  }}).join('');
  searchDropdown.style.display = 'block';
}});

function pickSearch(id) {{
  searchDropdown.style.display = 'none';
  searchInput.value = '';
  setFocusNode(id);
}}

document.addEventListener('click', e => {{
  if (!searchDropdown.contains(e.target) && e.target !== searchInput) {{
    searchDropdown.style.display = 'none';
  }}
}});

// KEYBOARD SHORTCUTS
window.addEventListener('keydown', e => {{
  if (e.target.tagName === 'INPUT') return;
  if (e.key === 'Escape') resetToOverview();
  if (e.key === '1') setHopDepth(1);
  if (e.key === '2') setHopDepth(2);
  if (e.key === '3') setHopDepth(3);
  if (e.key === 't' || e.key === 'T') toggleTests();
  if (e.key === 'f' || e.key === 'F') fitView();
}});

// INITIALIZE
setupFilterUI();
recomputeGraph();
resizeCanvas();
fitView();

// Auto focus on primary Candidate hub to start in focus mode
if (nodeMap.has('backend_app_models_candidate_candidate')) {{
  selectNode('backend_app_models_candidate_candidate');
}}
</script>

</body>
</html>
"""


def main():
    repo_root = Path(__file__).resolve().parent.parent
    graph_json = repo_root / "graphify-out" / "graph.json"
    output_html = repo_root / "graphify-out" / "hirely-explorer.html"

    if not graph_json.exists():
        print(f"Error: {graph_json} not found.", file=sys.stderr)
        sys.exit(1)

    result = build_explorer(graph_json, output_html)
    print("\n--- Summary ---")
    print(f"Output File: {result['output_path']}")
    print(f"Nodes Processed: {result['total_nodes']}")
    print(f"Edges Processed: {result['total_edges']}")
    print(f"Communities: {result['communities_count']}")
    print("Layer Breakdown:")
    for l, c in sorted(result['layer_counts'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {l}: {c}")


if __name__ == "__main__":
    main()
