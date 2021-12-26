import numpy as np
import matplotlib.pyplot as plt


# Inicializando a matriz que será a malha para nossos autômatos
def init_matrix(rows: int, cols: int):
	
	''' Initializes matrix with all zeros.
        
        Input:
            rows (int): number of rows;
            cols (int): number of cols.
        Output:
            mat ((int, int)): initialized matrix with all zeros. '''
	
	return np.zeros((rows, cols), dtype=int)

# Retorna o array com o impulso inicial, fornecido pelo usuário como parâmetro
def config_impulse(impulse_type: str, size: int, k: int):

    ''' Documentation '''
    
    #k = 3

    first_impulse = np.zeros(size, dtype=int)
    impulse_str = impulse_type.lower()

    if impulse_str == "custom":
        
        print("\nCustom seed must be the decimal codification of the array of alive cells.")
        aux_seed = int(input("SEED: "))

        str_seed = np.base_repr(aux_seed, base=k)
        for i in range(1, len(str_seed) + 1):
            first_impulse[-i] = int(str_seed[-i])
    
    elif impulse_str == "random":
        first_impulse = np.random.choice(range(k), size=size)

    else:
        start = int(input("Value of initial cell (0 <= val < {}): ".format(k)))

        if impulse_str == "left":
            index = 1
        elif impulse_str == "right":
            index = size - 2
        else: #impulse_str == "center":
            index = size // 2

        first_impulse[index] = start

    return first_impulse

# Cria o array com os bits da regra
def rule_array(rule_num: int, r: int, k: int):
    
    ''' Documentation '''

    #r = 1
    #k = 2

    nbhd = 2*r + 1          # nbhd: neighborhood
    pstt = k ** nbhd        # pstt: possible states

    rule_arr = np.zeros(pstt, dtype=int)
    rule_str = np.base_repr(rule_num, base=k, padding=pstt)[-pstt:]

    for i in range(pstt):
        rule_arr[i] = int(rule_str[ -(i + 1) ])     # Garantir que isso dá certo
    
    return rule_arr

# Realiza o cálculo de gerações para a matriz de autômatos
def gen_calc(matrix: np.ndarray, num_gen: int, rule_arr: np.ndarray, r: int):

    ''' Documentation '''
    
    #r = 1
    #k = 2

    # nbhd: neighborhood
    nbhd      = 2*r + 1
    size_gen  = len(matrix[0])
    mid_index = nbhd // 2
    POWERS_2  = np.array(  list(map(lambda x: 2**x, range(nbhd))), dtype=int  )

    for i in range(num_gen - 1):
        next_index = np.zeros(size_gen, dtype=int)
        
        gen = matrix[i]
        for j in range(1, r + 1):
            next_index += POWERS_2[mid_index + j] * np.roll(gen,  j)
            next_index += POWERS_2[mid_index - j] * np.roll(gen, -j)
        next_index += POWERS_2[mid_index] * gen
        
        matrix[i+1] = np.take(rule_arr, next_index)
    
    return matrix

# Plotta o gráfico de evolução dos autômatos
def plot_automata(matrix: np.ndarray):

    ''' Plots the cellular automaton matrix. 
        
        Input:
            matrix (array): matrix to be plotted.
        Output:
            None (window is created with the correct plot). '''

    plt.rcParams['image.cmap'] = 'binary'

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.matshow(matrix)
    ax.axis(False)
    plt.show()

# Envelope para rodar a lógica de evolução dos autômatos celulares
def run_automata(rule: int, num_gen: int, seed: str, r: int, k: int):

    ''' Documentation '''
    
    rule_index = rule_array(rule, r, k)

    size_gen = 2 * num_gen + 1
    matrix_ca = init_matrix(num_gen, size_gen)
    matrix_ca[0] = config_impulse(seed, size_gen, k)

    return gen_calc(matrix_ca, num_gen, rule_index, r)

if __name__ == "__main__":
    
    r = int(input("NEIGHBORHOOD SIZE (r): "))
    k = int(input("NUMBER OF CELL STATES (0..k): "))

    RULE = int(input("\nRULE: "))
    GEN  = int(input("NUMBER OF GENERATIONS: "))
    IMPL = input("IMPULSE [\"left\", \"center\", \"right\", \"custom\" or \"random\"]: ")

    MATRIX = run_automata(RULE, GEN, IMPL, r, k)
    plot_automata(MATRIX)
