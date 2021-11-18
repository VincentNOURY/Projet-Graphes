def define_matrix(lines : list) -> (int, int, list):
    for i in range(len(lines)):
        if lines[i][-1:] == "\n":
            lines[i] = lines[i][:-1]
    return int(lines[0]), int(lines[1]), lines[2:]

def read_matrix(path):
    with open(path, "r", encoding="utf-8") as file:
        return define_matrix(file.readlines())

def edges_treatment(matrix : list):
    for i in range(len(matrix)):
        matrix[i] = matrix[i].split(" ")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = int(matrix[i][j])

def spacing(matrix : list) -> int:
    maximum = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if len(str(matrix[i][j])) > maximum:
                maximum = len(str(matrix[i][j]))
    return maximum + 2

def print_matrix(matrix : list):
    space = spacing(matrix) # max(matrix) + 2
    for i in range(len(matrix)):
        line = ""
        for j in range(len(matrix[i])):
            line += str(matrix[i][j]).center(space," ") #+ (" " * (space % 2 + 1))
        print(line)
    print("\n")

def convert_to_adj(nbr_vertices : int, edges : list) -> list:
    adjacency_matrix = [[float('inf') if i != j else\
    0 for j in range(nbr_vertices)] for i in range(nbr_vertices)]
    for edge in edges:
        adjacency_matrix[edge[0]][edge[1]] = edge[2]
    return adjacency_matrix

def floyd_warshall(adjacency_matrix : list) -> (list, list):
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

def contains_negative_circle(matrix : list) -> bool:
    for i in range(len(matrix)):
        if matrix[i][i] < 0:
            return True
    return False

def shortest_path(p_matrix : list):
    for i in range(len(p_matrix)):
        for j in range(len(p_matrix[i])):
            list_for_path = []
            if p_matrix[i][j] < float('inf'):
                print(f"Le plus court chemin de {i} a {j} est :")
                list_for_path.append(j)
                while list_for_path[-1] != i:
                    list_for_path.append(p_matrix[i][list_for_path[-1]])
                list_for_path.reverse()
                print(str(list_for_path)[1:-1].replace(",", " ->"))
            else:
                print(f"Il n'existe pas de chemin entre {i} et {j}.")

def main():
    while True:
        print("Veuillez entrer l'identifiant de la matrice :")
        matrix_info = read_matrix(f"matrix{int(input())}.txt")
        nbr_vertices = matrix_info[0]
        edges = matrix_info[2]
        edges_treatment(edges)
        adjacency_matrix = convert_to_adj(nbr_vertices, edges)
        print("Affichage de la matrice d'adjacence : ")
        print_matrix(adjacency_matrix)

        fl_result, p_matrix = floyd_warshall(adjacency_matrix)
        if contains_negative_circle(fl_result):
            print("Ce graphe contient un cycle absorbant.")
        else:
            shortest_path(p_matrix)
        print("Souhaitez-vous continuer (y/n) ?")
        if input().lower() != "y":
            break

if __name__ == "__main__":
    main()
