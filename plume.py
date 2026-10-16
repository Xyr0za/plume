import argparse

from engine import build_edge_weights, compute_geometry, render_tree


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Collatz conjecture coral visualizations.")
    parser.add_argument("-n", "--limit", type=int, default=10000, help="Maximum starting integer (default: 10000)")
    parser.add_argument("-e", "--even-angle", type=float, default=8.65, help="Turn angle in degrees for even nodes (default: 8.65)")
    parser.add_argument("-d", "--odd-angle", type=float, default=-16.0, help="Turn angle in degrees for odd nodes (default: -16.0)")
    parser.add_argument("-o", "--output", type=str, default="collatz_coral.png", help="Output file path (default: collatz_coral.png)")
    parser.add_argument("--dpi", type=int, default=300, help="Output image DPI (default: 300)")
    parser.add_argument("-c", "--cmap", type=str, default="magma", help="Matplotlib colormap name (default: magma)")
    parser.add_argument("--bg-color", type=str, default="#05060f", help="Background hex color (default: #05060f)")
    parser.add_argument("-s", "--size", type=float, default=12.0, help="Figure dimension in inches (default: 12.0)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output")
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.quiet:
        print(f"Computing Collatz sequences up to {args.limit}...")
    edge_weights = build_edge_weights(args.limit)

    if not args.quiet:
        print(f"Calculating geometry for {len(edge_weights)} unique segments...")
    segments, traffic, depths = compute_geometry(edge_weights, args.even_angle, args.odd_angle)

    if not args.quiet:
        print("Rendering...")
    render_tree(segments, traffic, depths, args.output, args.dpi, args.cmap, args.bg_color, args.size)

    if not args.quiet:
        print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()