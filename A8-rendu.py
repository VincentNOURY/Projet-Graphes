"""
Description : Takes a representation of a graph with weights and applies
              the floyd-Warshall algorithm to print the shortest path
              for each point.

Usage : python3 "A8-rendu.py"
        will ask the user which matrix to use (indices goes from -1 to 13)

Arguments : None
"""


def define_matrix(lines: list) -> (int, int, list):
    """
    Description : Defines a matrix, number of vertices and number of edges
                  based on the read data

    Arguments :
        - lines (2D string list) : a list of string read from the file

    Result : Returns (int, int, list) representing respectively number of
             vertices, number of edges and the matrix as in the read file
             (trailing end of lines removed)
    """

    for index, element in enumerate(lines):
        if element[-1:] == "\n":
            lines[index] = element[:-1]
    return int(lines[0]), int(lines[1]), lines[2:]


def read_matrix(path: str) -> (int, int, list):
    """
    Description : Reads the file from the given path

    Arguments :
        - path (String) : path/to/the/file

    Result : Returns the result of define_matrix
    """

    with open(path, "r", encoding="utf-8") as file:
        return define_matrix(file.readlines())


def edges_treatment(matrix: list):
    """
    Description : Modify the matrix to convert strings to int lists

    Arguments :
        - matrix (2D string list) : the matrix to sanitize

    Result : Returns nothing modify directly the matrix
    """

    for index, element in enumerate(matrix):
        matrix[index] = element.split(" ")
    for index, line in enumerate(matrix):
        for jndex, element in enumerate(line):
            matrix[index][jndex] = int(element)


def spacing(matrix: list) -> int:
    """
    Description : Defines the spacing for the printing of the matrix

    Arguments :
        - matrix (2D list) : the matrix you want to print

    Result : Returns the spacing needed to print the matrix correctly
    """

    maximum = 0
    for line in matrix:
        for element in line:
            if len(str(element)) > maximum:
                maximum = len(str(element))
    return maximum + 2


def print_matrix(matrix: list):
    """
    Description : Prints a given matrix (2D list), the spacing is defined by
                  the sapcing function

    Arguments :
        - matrix (2D list) : the matrix you want to print

    Result : Prints the matrix
    """

    space = spacing(matrix)  # max(matrix) + 2
    for line in matrix:
        line_to_print = ""
        for element in line:
            line_to_print += str(element).center(space, " ")
            # + (" " * (space % 2 + 1))
        print(line_to_print)
    print("\n")


def convert_to_adj(nbr_vertices: int, edges: list) -> list:
    """
    Description : Converts the representation of the matrix to an adjacency
                  matrix

    Arguments :
        - nbr_vertices (int) : the number of vertices in the graph
        - edges (2D int list) : the treated matrix

    Result : Returns an adjacency matrix
    """

    adjacency_matrix = [[float('inf') if i != j else 0
                        for j in range(nbr_vertices)]
                        for i in range(nbr_vertices)]
    for edge in edges:
        adjacency_matrix[edge[0]][edge[1]] = edge[2]
    return adjacency_matrix


def floyd_warshall(adjacency_matrix: list) -> (list, list):
    """
    Description : floyd-warshall's algorithm

    Arguments :
        - adjacency_matrix (2D int list) : the adjacency matrix of the graph
                                       you want to apply the algorithm on.

    Result : Returns the two matrix (2D lists) after the iterations of
             the algorithm
    """

    nb_of_edges = len(adjacency_matrix)
    w_matrix = adjacency_matrix[:]
    p_matrix = [[i for j in range(nb_of_edges)] for i in range(nb_of_edges)]
    for k in range(nb_of_edges):
        for i in range(nb_of_edges):
            for j in range(nb_of_edges):
                if w_matrix[i][j] > w_matrix[i][k] + w_matrix[k][j]:
                    w_matrix[i][j] = w_matrix[i][k] + w_matrix[k][j]
                    p_matrix[i][j] = p_matrix[k][j]
        print(f"Matrice L a l'iteration {k} :")
        print_matrix(adjacency_matrix)
        print(f"Matrice P a l'iteration {k} :")
        print_matrix(p_matrix)
    return w_matrix, p_matrix


def contains_negative_circle(matrix: list) -> bool:
    """
    Description : Checks if the graph contains a negative cycle

    Arguments :
        - matrix (2D int list) : the adjacency matrix after the iterations of
                                 the floyd-warshall algorithm

    Result : Returns boolean
    """

    for index, value in enumerate(matrix):
        if value[index] < 0:
            return True
    return False


def shortest_path(p_matrix: list, l_matrix: list):
    """
    Descrition : Displays the sortest path from a point A to a point B

    Arguments :
        - p_matrix (2D int list) : the P matrix after floyd-warshall algorithm
        - l_matrix (2D int list) : the L matrix after floyd-warshall algorithm

    Result : Prints every path
    """

    for index, line in enumerate(p_matrix):
        for jndex in range(len(line)):
            list_for_path = []
            if str(l_matrix[index][jndex]) != "inf":
                print(f"Le plus court chemin de {index} a {jndex} est :")
                list_for_path.append(jndex)
                while list_for_path[-1] != index:
                    list_for_path.append(line[list_for_path[-1]])
                list_for_path.reverse()
                print(str(list_for_path)[1:-1].replace(",", " ->"))
            else:
                print(f"Il n'existe pas de chemin entre {index} et {jndex}.")


def main():
    """
    Description : Main function

    Arguments : None

    Result : Uses the floyd-warshall algorithm to display the shortest path
             from every point to every other point.
    """

    while True:
        print("Veuillez entrer l'identifiant de la matrice :")
        matrix_info = read_matrix(f"A8-graph{int(input())}.txt")
        nbr_vertices = matrix_info[0]
        edges = matrix_info[2]
        edges_treatment(edges)
        adjacency_matrix = convert_to_adj(nbr_vertices, edges)
        print("Affichage de la matrice d'adjacence : ")
        print_matrix(adjacency_matrix)

        l_matrix, p_matrix = floyd_warshall(adjacency_matrix)
        if contains_negative_circle(l_matrix):
            print("Ce graphe contient un cycle absorbant.")
        else:
            shortest_path(p_matrix, l_matrix)
        print("Souhaitez-vous continuer (y/n) ?")
        if input().lower() != "y":
            break


if __name__ == "__main__":
    main()
