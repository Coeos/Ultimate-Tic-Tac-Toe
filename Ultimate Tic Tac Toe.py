# -*- coding: utf-8 -*-
"""
Created on Sun May 14 15:29:11 2023

@author: eliot
"""
import numpy as np
import copy
import random

class Plateau():

    def __init__(self):
        self.matrice = np.empty((3, 3), dtype=object)
        self.current_player = 'O'
        self.nb_sous_matrices_gagnés = {'O' : 0 , 'X' :0}
        self.sous_matrices_gagnés=[[False for i in range(3)]for j in range(3)]
        self.prochaine_grille = None
        
                
    def jouer_case(self,sous_matrice_i,sous_matrice_j,case_i,case_j):
        
        if self.matrice[sous_matrice_i][sous_matrice_j][case_i][case_j] == ' ':
            self.matrice[sous_matrice_i][sous_matrice_j][case_i][case_j] = self.current_player
            self.condition(sous_matrice_i, sous_matrice_j)
            self.current_player = 'X' if self.current_player == 'O' else 'O'
            self.prochaine_grille =[case_i,case_j]
            if self.sous_matrices_gagnés[sous_matrice_i][sous_matrice_j] == True:
                self.prochaine_grille = None 
            ##self.afficher()
        else :
            print("mauvaise sélection")
                    
    def remplir_matrice_gagné (self,x,y):
        self.sous_matrices_gagnés[x][y] = True
        self.nb_sous_matrices_gagnés[self.current_player] += 1
        return  [[self.current_player for i in range(3)] for j in range(3)]
        
    
    
    def condition (self, x,y):
           
            for k in range (3):
                if self.matrice[x,y][0][k] == self.matrice[x,y][1][k] == self.matrice[x,y][2][k] != ' ' or self.matrice[x,y][k][0] == self.matrice[x,y][k][1] == self.matrice[x,y][k][2] != ' ' :
                    self.matrice[x,y] = self.remplir_matrice_gagné(x,y)
                  
            if self.matrice[x,y][0][0] == self.matrice[x,y][1][1] == self.matrice[x,y][2][2] != ' ' or self.matrice[x,y][0][2] == self.matrice[x,y][1][1] == self.matrice[x,y][2][0] != ' ':
                    self.matrice[x,y] = self.remplir_matrice_gagné(x,y)
            if all(case != ' ' for ligne in self.matrice[x][y] for case in ligne) and self.sous_matrices_gagnés[x][y] == False :
                
                self.sous_matrices_gagnés[x][y] = False
    def fin_partie(self):
        for i in self.nb_sous_matrices_gagnés.keys():
            if self.nb_sous_matrices_gagnés[i] == 3:
                for a  in range (3):
                    for b  in range (3):
                        for c  in range (3):
                            for d in range (3):
                                self.matrice[a][b][c][d] = i
                return True 
            
    def afficher(self):
        for i in range(3):
            print("\n" + "===+===+=== " * 3)
            for j in range(3):
                print(" {} | {} | {} ".format(
                    self.matrice[i][j][0][0],
                    self.matrice[i][j][0][1],
                    self.matrice[i][j][0][2]
                ), end=" ")
            print("\n" + "----------- " * 3)
            for j in range(3):
                print(" {} | {} | {} ".format(
                    self.matrice[i][j][1][0],   
                    self.matrice[i][j][1][1],
                    self.matrice[i][j][1][2]
                ), end=" ")
            print("\n" + "----------- " * 3)
            for j in range(3):
                print(" {} | {} | {} ".format(
                    self.matrice[i][j][2][0],
                    self.matrice[i][j][2][1],
                    self.matrice[i][j][2][2]
                ), end=" ")
        print("\n" + "===+===+=== " * 3)
        
        
        
        
        
 ## Partie IA
       
    def coup_possibles (self):
        if self.prochaine_grille == None:
            possible_moves = []
            for i in range(3):
                for j in range(3):
                    if not self.sous_matrices_gagnés[i][j]:
                        for x in range(3):
                            for y in range(3):
                                if self.matrice[i][j][x][y] == ' ':
                                    possible_moves.append((i, j, x, y))
            return possible_moves
        else:
            return [(self.prochaine_grille[0], self.prochaine_grille[1], x, y) for x in range(3) for y in range(3) if self.matrice[self.prochaine_grille[0]][self.prochaine_grille[1]][x][y] == ' ']

    def copy(self):
        return copy.deepcopy(self)

    def heuristique(self, player):
        opponent = 'X' if player == 'O' else 'O'
        total_score = 0
    
        # Évaluation de chaque sous-grille
        for i in range(3):
            for j in range(3):
                if not self.sous_matrices_gagnés[i][j]:
                    # Évaluation des lignes
                    for x in range(3):
                        total_score += score_line(self.matrice[i][j][x, :], player)
                    # Évaluation des colonnes
                    for y in range(3):
                        total_score += score_line(self.matrice[i][j][:, y], player)
                    # Évaluation des diagonales
                    total_score += score_line(np.diag(self.matrice[i][j]), player)
                    total_score += score_line(np.diag(np.fliplr(self.matrice[i][j])), player)
    
        # Si prochaine_grille n'est pas None, évaluer également la grille où l'adversaire va jouer ensuite
        if self.prochaine_grille is not None:
            i, j = self.prochaine_grille
            if not self.sous_matrices_gagnés[i][j]:
                # Évaluation des lignes
                for x in range(3):
                    total_score += score_line(self.matrice[i][j][x, :], opponent)
                # Évaluation des colonnes
                for y in range(3):
                    total_score += score_line(self.matrice[i][j][:, y], opponent)
                # Évaluation des diagonales
                total_score += score_line(np.diag(self.matrice[i][j]), opponent)
                total_score += score_line(np.diag(np.fliplr(self.matrice[i][j])), opponent)
    
        return total_score
    
    def minimax(self, profondeur, alpha, beta, maximizingPlayer, player):
        if profondeur == 0 or self.fin_partie():
            return self.heuristique(player), None
    
        if maximizingPlayer:
            maxEval = float('-inf')
            coupChoisi = None
            for move in self.coup_possibles():
                new_plateau = self.copy()
                new_plateau.jouer_case(*move)
                eval = new_plateau.minimax(profondeur-1, alpha, beta, False, 'O' if player == 'X' else 'X')[0]
                
                if eval > maxEval:
                    maxEval = eval
                    coupChoisi = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, coupChoisi
    
        else:
            minEval = float('inf')
            coupChoisi = None
            for move in self.coup_possibles():
                new_plateau = self.copy()
                new_plateau.jouer_case(*move)
                eval = new_plateau.minimax(profondeur-1, alpha, beta, True, 'O' if player == 'X' else 'X')[0]
                
                if eval < minEval:  
                    minEval = eval
                    coupChoisi = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, coupChoisi

def score_line(line, player):
    
        # Coefficients pour différentes configurations
        THREE_IN_A_ROW = 1000
        TWO_IN_A_ROW = 25
        ONE_IN_A_ROW = 1
        OPPONENT_TWO_IN_A_ROW = -100
        OPPONENT_ONE_IN_A_ROW = -1
        opponent = 'X' if player == 'O' else 'O'
        countP = 0
        for element in line:
            if element == player:
                countP += 1
        countO = 0
        for element in line:
            if element == opponent:
                countO += 1
            # Si le joueur a une ligne gagnante, il obtient le plus grand score.
        if countP == 3:
            return THREE_IN_A_ROW
        # Si le joueur a deux en ligne et que l'adversaire n'a pas bloqué, il obtient un score élevé.
        elif countP == 2 and countO == 0:
            return TWO_IN_A_ROW
        # Si le joueur a un en ligne et que l'adversaire n'a pas bloqué, il obtient un score faible.
        elif countP == 1 and countO <=1:
            return ONE_IN_A_ROW
        # Si l'adversaire a deux en ligne, le joueur obtient un score négatif.
        elif countO == 2 and countP == 0:
            return OPPONENT_TWO_IN_A_ROW
        # Si l'adversaire a un en ligne, le joueur obtient un score légèrement négatif.
        elif countO == 1 and countP <=1 :
            return OPPONENT_ONE_IN_A_ROW
        else:
            return 0
        
    


def main() :
    
    plateau = Plateau()
    for i in range(3):
        for j in range(3):
            plateau.matrice[i, j] = np.array([[' ' for i in range(3)]for j in range(3)])
    
    is_maximizing = False
    depth = 4 # Vous pouvez ajuster cette valeur pour changer la profondeur de recherche de l'algorithme minimax

    while not plateau.fin_partie():
        if plateau.prochaine_grille == None:
            if is_maximizing:
                x, y, i, j = input("Veuillez entrer les valeurs de x, y, i et j : ").split()
                x = int(x)
                y = int(y)
                i = int(i)
                j = int(j)
                plateau.jouer_case(x, y, i, j)
                is_maximizing = not is_maximizing
            else:
                print("Tour de l'IA (O)")
                _, move = plateau.minimax( depth,  float('-inf'), float('inf'),is_maximizing, plateau.current_player)
                
                if move is not None:
                    plateau.jouer_case(*move)
                else:
                    print("Meilleur coup introuvable, l'IA joue un coup aléatoire.")
                    possible_moves = plateau.coup_possibles()
                    if possible_moves:
                        random_move = random.choice(possible_moves)
                        plateau.jouer_case(*random_move)
                    else:
                        print("Erreur: aucun coup possible.")
                        break
                is_maximizing = not is_maximizing
        else:
            if is_maximizing:
                i, j = input("Veuillez entrer les valeurs de ligne et colonne : ").split()
                i = int(i)
                j = int(j)
                plateau.jouer_case(plateau.prochaine_grille[0], plateau.prochaine_grille[1], i, j)
                is_maximizing = not is_maximizing
            else:
                print("Tour de l'IA (O)")
                _, move = plateau.minimax(  depth,  float('-inf'), float('inf'),is_maximizing, plateau.current_player)
                
                if move is not None:
                    plateau.jouer_case(*move)
                else:
                    print("Meilleur coup introuvable, l'IA joue un coup aléatoire.")
                    possible_moves = plateau.coup_possibles()
                    if possible_moves:
                        random_move = random.choice(possible_moves)
                        plateau.jouer_case(*random_move)
                    else:
                        print("Erreur: aucun coup possible.")
                        break
                is_maximizing = not is_maximizing
        plateau.afficher()

  

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    