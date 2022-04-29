from register_allocation_using_graph_coloring import *

def test_no_spilling():

    instructions = [
        "a := b + c",
        "d := a",
        "e := d + f",
        "f := 2 + e",
        "b := d + e",
        "e := e - 1",
        "b := f + c"
    ]

    G = construct_graph_from_instructions(instructions)

    print("Graph:")
    print(G.nodes)
    print(G.edges)
    print()

    plot_graph(G, title="Constructed graph")

    solution = graph_coloring(G, 4)

    print("Solution:")

    print({n:COLORS[solution[i]-1] for i,n in enumerate(G.nodes)})

    if solution:
        plot_graph(G, color_map=[COLORS[ci-1] for ci in solution], title="Coloring solution")




def test_spilling():

    instructions = [
        "a := b + c",
        "d := a",
        "e := d + f",
        "f := 2 + e",
        "b := d + e",
        "e := e - 1",
        "b := f + c",
        "a := e"
    ]

    G = construct_graph_from_instructions(instructions)

    print("Graph:")
    print(G.nodes)
    print(G.edges)
    print()

    plot_graph(G, title="Constructed graph")

    while True:
        solution = graph_coloring(G, 3)
        if solution:
            break
        else:
            G = spilling_graph(G)
            plot_graph(G, title="Spilling graph")

    print("Solution:")

    print({n:COLORS[solution[i]-1] for i,n in enumerate(G.nodes)})

    if solution:
        plot_graph(G, color_map=[COLORS[ci-1] for ci in solution], title="Coloring solution")


if __name__ == "__main__":
    test_no_spilling()
    # test_spilling()
