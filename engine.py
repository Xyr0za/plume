from collections import defaultdict, deque

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection


def build_edge_weights(limit):
    edge_weights = defaultdict(int)
    for start_node in range(1, limit + 1):
        curr = start_node
        path = [curr]
        while curr > 1:
            curr = curr // 2 if curr % 2 == 0 else 3 * curr + 1
            path.append(curr)

        path.reverse()
        for i in range(len(path) - 1):
            edge_weights[(path[i], path[i + 1])] += 1

    return edge_weights


def compute_geometry(edge_weights, even_angle, odd_angle):
    even_rad = np.radians(even_angle)
    odd_rad = np.radians(odd_angle)

    adjacency = defaultdict(list)
    for parent, child in edge_weights:
        adjacency[parent].append(child)

    node_states = {1: (0.0, 0.0, np.pi / 2, 0)}
    frontier = deque([1])

    segments = []
    traffic = []
    depths = []

    while frontier:
        parent = frontier.popleft()
        x1, y1, angle, depth = node_states[parent]

        for child in adjacency[parent]:
            next_angle = angle + (even_rad if child % 2 == 0 else odd_rad)
            length = 1.0 / (np.log10(child + 2) ** 0.35)

            x2 = x1 + np.cos(next_angle) * length
            y2 = y1 + np.sin(next_angle) * length

            node_states[child] = (x2, y2, next_angle, depth + 1)
            frontier.append(child)

            segments.append([(x1, y1), (x2, y2)])
            traffic.append(edge_weights[(parent, child)])
            depths.append(depth + 1)

    return segments, np.array(traffic, dtype=float), np.array(depths, dtype=float)


def render_tree(segments, traffic, depths, output_path, dpi, colormap, bg_color, fig_size):
    log_traffic = np.log1p(traffic) / np.log1p(traffic.max())
    norm_depths = depths / depths.max()

    color_blend = 0.65 * (1.0 - norm_depths) + 0.35 * log_traffic
    widths = 0.15 + 3.0 * (log_traffic ** 1.6)
    opacities = 0.18 + 0.82 * (log_traffic ** 0.7)

    cmap = plt.get_cmap(colormap)
    colors = cmap(0.15 + 0.83 * color_blend)
    colors[:, 3] = opacities

    fig, ax = plt.subplots(figsize=(fig_size, fig_size), facecolor=bg_color)
    ax.set_facecolor(bg_color)

    glow_mask = log_traffic > 0.25
    glow_segments = [seg for seg, keep in zip(segments, glow_mask) if keep]
    glow_colors = colors[glow_mask].copy()
    glow_colors[:, 3] = 0.08 * log_traffic[glow_mask]
    glow_widths = widths[glow_mask] * 3.5

    ax.add_collection(LineCollection(
        glow_segments, colors=glow_colors, linewidths=glow_widths, capstyle="round"
    ))
    ax.add_collection(LineCollection(
        segments, colors=colors, linewidths=widths, capstyle="round"
    ))

    ax.autoscale()
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout(pad=0.2)
    plt.savefig(output_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
