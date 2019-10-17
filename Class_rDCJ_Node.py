import copy
import numpy as np

class Node:

    def __init__(self, state=None):
        self.state = state
        self.children = []
        self.linear_chromosomes = []
        self.circular_chromosomes = []
        self.next_operation = 0

        get_chromosomes = Node.find_chromosomes(self, self.state)
        self.linear_chromosomes = get_chromosomes[0]
        self.circular_chromosomes = get_chromosomes[1]



    def find_next_extremity(self, current, next_extremity):
        if current[0] == next_extremity:
            if current[1] % 1 == 0:
                next = current[1] + 0.5
            else:
                next = current[1] - 0.5
        else:
            if current[0] % 1 == 0:
                next = current[0] + 0.5
            else:
                next = current[0] - 0.5
        return next

    def find_next_adjacency(self, next_extremity, chromosome, not_telomeres):
        for element in not_telomeres:
            if element[0] == next_extremity or element[1] == next_extremity:
                current = element
                chromosome.append(current)
                not_telomeres.remove(current)
                next_extremity = Node.find_next_extremity(self, current, next_extremity)
                return next_extremity, chromosome, not_telomeres
        return [next_extremity]

    def find_adjacency_cycle(self, next_extremity, chromosome, not_telomeres):


        next_adjacency = Node.find_next_adjacency(self, next_extremity, chromosome, not_telomeres)

        while len(next_adjacency) != 1:

            next_extremity = next_adjacency[0]
            next_adjacency = Node.find_next_adjacency(self, next_extremity, chromosome, not_telomeres)


        else:
            next_extremity = next_adjacency[0]

            return next_extremity, chromosome, not_telomeres

    def find_chromosomes(self, adjacencies):
        telomeres = [element for element in adjacencies if type(element) is not tuple]
        not_telomeres = [element for element in adjacencies if type(element) is tuple]

        linear_chromosomes = []
        circular_chromosomes = []
        chromosome = []
        i = 0

        # find linear chromosomes
        while len(telomeres) > 0:

            i += 1
            current = telomeres[0]

            telomeres.remove(current)
            chromosome.append(current)

            if current % 1 == 0:
                next_extremity = current + 0.5
            else:
                next_extremity = current - 0.5

            # if single gene chromosome
            if next_extremity in telomeres:
                current = next_extremity

                telomeres.remove(current)
                chromosome.append(current)
                linear_chromosomes.append(chromosome)
                chromosome = []

            # else find adjacency cycle
            else:
                adjacency_cycle = Node.find_adjacency_cycle(self, next_extremity, chromosome, not_telomeres)
                next_extremity = adjacency_cycle[0]

                if next_extremity in telomeres:
                    current = next_extremity
                    telomeres.remove(current)
                    chromosome.append(current)
                    linear_chromosomes.append(chromosome)
                    chromosome = []

        # find circular chromosomes
        while len(not_telomeres) > 0:
            current = not_telomeres[0]
            not_telomeres.remove(current)
            chromosome.append(current)

            # find next extremity:
            if current[0] % 1 == 0:
                next_extremity = current[0] + 0.5
            else:
                next_extremity = current[0] - 0.5

            # if it is a single gene chromosome:
            if next_extremity == current[1]:
                ordered_circular_chromosome = []

                circular_chromosomes.append(chromosome)
                chromosome = []

            # go find adjacency cycle
            else:
                adjacency_cycle = Node.find_adjacency_cycle(self, next_extremity, chromosome, not_telomeres)
                next_extremity = adjacency_cycle[0]

                # if at end of circular chromosome
                if next_extremity == chromosome[0][1]:
                    ordered_circular_chromosome =[]

                    circular_chromosomes.append(chromosome)
                    chromosome = []
                    print()
        return linear_chromosomes, circular_chromosomes




    def get_legal_operations(self, adjacenciesB):
        list_of_legal_operations = []
        adjacenciesA = self.state
        adjacenciesB = adjacenciesB

        for element in adjacenciesB:
            adjacenciesA_copy = copy.deepcopy(adjacenciesA)

            # if element is an adjacency:
            if type(element) is tuple:
                p = element[0]
                q = element[1]
                u = 0
                v = 0

                # if elements containing p and q respectively in a are adjacencies
                for marker in adjacenciesA_copy:
                    if type(marker) is tuple:
                        if marker[0] == p or marker[1] == p:
                            u = marker

                        if marker[0] == q or marker[1] == q:
                            v = marker

                # element containing p in A is a telomere
                if u == 0:
                    u = p
                # element containing q in A is a telomere
                if v == 0:
                    v = q

                if u != v:
                    adjacenciesA_copy.append((p, q))
                    adjacenciesA_copy.remove(u)
                    adjacenciesA_copy.remove(v)

                    # if u is an adjacency:
                    if type(u) is tuple:
                        # calcultate u'p
                        if u[0] == p:
                            u_not_p = u[1]
                        else:
                            u_not_p = u[0]

                        # if v is an adjacency:
                        if type(v) is tuple:
                            # calcultate v'q
                            if v[0] == q:
                                v_not_q = v[1]
                            else:
                                v_not_q = v[0]

                            adjacenciesA_copy.append((u_not_p, v_not_q))
                            operation = ((u, v), ((p, q), (u_not_p, v_not_q)))

                            # order operation before appending
                            op_1 = 0
                            op_2_1 = 0
                            op_2_2 = 0
                            op_2 = 0

                            if u[0] < v[0]:
                                op_1 = (u, v)
                            else:
                                op_1 = (v, u)
                            if p < q:
                                op_2_1 = (p, q)
                            else:
                                op_2_1 = (q, p)
                            if u_not_p < v_not_q:
                                op_2_2 = (u_not_p, v_not_q)
                            else:
                                op_2_2 = (v_not_q, u_not_p)
                            if op_2_1[0] < op_2_2[0]:
                                op_2 = (op_2_1, op_2_2)
                            else:
                                op_2 = (op_2_2, op_2_1)
                            ordered_operation = (op_1, op_2)

                            if ordered_operation not in list_of_legal_operations:
                                list_of_legal_operations.append((ordered_operation))
                            else:
                                pass


                        # else v is a telomere
                        else:
                            adjacenciesA_copy.append(u_not_p)
                            operation = ((u, v), ((p, q), (u_not_p)))
                            # if u[0] < v:
                            #    op_1 = (u, v)
                            # else:
                            #    op_1 = (v, u)
                            if p < q:
                                op_2_1 = (p, q)
                            else:
                                op_2_1 = (q, p)
                                # if op_2_1[0] < u_not_p:
                                op_2 = (op_2_1, u_not_p)
                            # else:
                            #    op_2 = (u_not_p, op_2_1)
                            op_2 = (op_2_1, u_not_p)
                            ordered_operation = ((u, v), op_2)

                            if ordered_operation not in list_of_legal_operations:
                                list_of_legal_operations.append((ordered_operation))
                            else:
                                pass


                    # else u is a telomere
                    else:
                        # if v is an adjacency
                        if type(v) is tuple:
                            # calculate v'q
                            if v[0] == q:
                                v_not_q = v[1]
                            else:
                                v_not_q = v[0]
                            adjacenciesA_copy.append(v_not_q)
                            operation = ((v, u), ((p, q), (v_not_q)))

                            if p < q:
                                op_2_1 = (p, q)
                            else:
                                op_2_1 = (q, p)

                            ordered_operation = ((v, u), (op_2_1, v_not_q))

                            if ordered_operation not in list_of_legal_operations:
                                list_of_legal_operations.append((ordered_operation))
                            else:
                                pass


                        # e;se v is a telomere
                        else:
                            operation = (u, v, ((p, q)))
                            if p < q:
                                op_2 = (p, q)
                            else:
                                op_2 = (q, p)
                            if u < v:
                                ordered_operation = (u, v, op_2)
                            else:
                                ordered_operation = (v, u, op_2)

                            if ordered_operation not in list_of_legal_operations:
                                list_of_legal_operations.append((ordered_operation))
                            else:
                                pass


            # else if the element is a telomere
            elif type(element) is str:
                u = 0
                p = element

                for marker in adjacenciesA_copy:
                    if type(marker) is tuple:
                        if marker[0] == p or marker[1] == p:
                            u = marker

                if u == 0:
                    u = p

                # if u is not a telomere:
                if u != p:
                    adjacenciesA_copy.append(u[0])
                    adjacenciesA_copy.append(u[1])
                    adjacenciesA_copy.remove(u)
                    operation = ((u), (u[0]), (u[1]))
                    if operation not in list_of_legal_operations:
                        list_of_legal_operations.append((operation))
                    else:
                        pass

        return list_of_legal_operations


    def take_action(self, operation):
        state_copy = copy.deepcopy(self.state)

        # if it is a fusion or fission:

        if len(operation) == 3:

            # fission
            if type(operation[0]) is tuple:

                state_copy.remove(operation[0])
                state_copy.append(operation[1])
                state_copy.append(operation[2])

            # fusion
            else:
                state_copy.remove(operation[0])
                state_copy.remove(operation[1])

                # ensure gene extremities in correct order for downstream comparisions with genome B extremities
                if operation[2][0] < operation[2][1]:
                    state_copy.append(operation[2])
                else:
                    state_copy.append((operation[2][1], operation[2][0]))

        # else it is another rearrangment
        elif len(operation) == 2:
            # transpositions, balanced translcations and block interchanges:
            # if type(operation[0]) is tuple and type(operation[-1]) is tuple:
            if type(operation[0][0]) is tuple and type(operation[0][1]) is tuple:
                state_copy.remove(operation[0][0])
                state_copy.remove(operation[0][1])

                # ensure gene extremities in correct order for downstream comparision with genome B extremities

                if operation[1][0][0] < operation[1][0][1]:
                    state_copy.append(operation[1][0])
                else:
                    state_copy.append((operation[1][0][1], operation[1][0][0]))

                if operation[1][1][0] < operation[1][1][1]:
                    state_copy.append(operation[1][1])
                else:
                    state_copy.append((operation[1][1][1], operation[1][1][0]))



            # unbalanced translocations and intrachromosomal transpositions to end of chromosome
            elif type(operation[0][0]) is not tuple or type(operation[0][-1]) is not tuple:

                state_copy.remove(operation[0][0])
                state_copy.remove(operation[0][1])

                # ensure gene extremities in correct order for downstream comparisions with genome B extremities
                if operation[1][0][0] < operation[1][0][1]:
                    state_copy.append(operation[1][0])
                else:
                    state_copy.append((operation[1][0][1], operation[1][0][0]))

                state_copy.append(operation[1][1])


        else:
            # RAISE AN ERROR
            print("YOU'VE GOT A PROBLEM DARLING")

        # order and sort
        ordered_and_sorted = Node.order_and_sort(self, state_copy)
        print('this is supposed to be ordered: ', ordered_and_sorted)

        return ordered_and_sorted


    def is_equivalent(self, adjacenciesB):
        adjacenciesA = copy.deepcopy(self.state)
        adjacenciesB = adjacenciesB

        ordered_adjacenciesA = []
        for element in adjacenciesA:
            if type(element) is tuple:
                if int(element[0]) < int(element[1]):
                    ordered_adjacenciesA.append(element)
                else:
                    ordered_adjacenciesA.append((element[1], element[0]))
            else:
                ordered_adjacenciesA.append(element)

        for element in adjacenciesB:
            if element in ordered_adjacenciesA:
                pass
            else:
                return False

        return True


    def order_adjacencies(self):
        ordered = []
        for element in self.state:
            if type(element) is tuple:
                if int(element[0]) < int(element[1]):
                    ordered.append(element)
                else:
                    ordered.append((element[1], element[0]))
            else:
                ordered.append(element)
        sort = []
        tuples = []
        not_tuples = []
        for element in ordered:
            if type(element) is tuple:
                tuples.append(element)
            else:
                not_tuples.append(element)
        for element in sorted(not_tuples):
            sort.append(element)
        for element in sorted(tuples):
            sort.append(element)

        self.state = sort

    def order_and_sort(self, adjacencies):
        ordered = []
        for element in adjacencies:
            if type(element) is tuple:

                #if it is a single gene adjacency e.g. (4.5, 4.0)
                if int(element[0]) == int(element[1]):
                    if element[0]%1 == 0:
                        ordered.append(element)
                    else:
                        ordered.append((element[1], element[0]))

                elif int(element[0]) < int(element[1]):
                    ordered.append(element)
                else:
                    ordered.append((element[1], element[0]))
            else:
                ordered.append(element)
        sort = []
        tuples = []
        not_tuples = []
        for element in ordered:
            if type(element) is tuple:
                tuples.append(element)
            else:
                not_tuples.append(element)
        for element in sorted(not_tuples):
            sort.append(element)
        for element in sorted(tuples):
            sort.append(element)

        return sort

    def get_Astar_heuristic(self, adjacenciesB):
        adjacenciesA = self.state
        adjacenciesB = adjacenciesB

        counter = 0
        for adj in adjacenciesB:
            if adj not in adjacenciesA:
                counter += 1

        heuristic = counter / 2
        return heuristic

    def check_if_operation_exists(self, circular_adjacency, adjacenciesB):
        list_of_legal_operations = []
        adjacenciesA = self.state


        #if it is not the adjacency of a single gene chromosome:
        if int(circular_adjacency[0]) != int(circular_adjacency[1]): # if it is not a single gene chromosome (otherwise next if will see it as final state e.g.: (4, 4.5)

            # if it is a final state adjacency:
            if circular_adjacency[0] + 0.5 == circular_adjacency[1] or circular_adjacency[0] - 0.5 == circular_adjacency[1]:

                return False

            else:

                adjacenciesA_copy = copy.deepcopy(adjacenciesA)

                a = circular_adjacency[0]
                b = circular_adjacency[1]
                if a%1 == 0:
                    a_partner = a-0.5
                else:
                    a_partner = int(a+0.5)
                if b%1 == 0:
                    b_partner = b-0.5
                else:
                    b_partner = int(b+0.5)

                if a_partner<b_partner:
                    circular_adjacency_partner = (a_partner, b_partner)
                else:
                    circular_adjacency_partner = (b_partner, a_partner)



                # if partner is an adjacency
                if circular_adjacency_partner in adjacenciesA_copy:
                    operation = ((circular_adjacency, circular_adjacency_partner), ((a, a_partner), (b, b_partner)))
                    # order operation
                    if circular_adjacency[0] < circular_adjacency_partner[0]:
                        op_1 = (circular_adjacency, circular_adjacency_partner)
                    else:
                        op_1 = (circular_adjacency_partner, circular_adjacency)

                    if a < a_partner:
                        op_2_1 = (a, a_partner)
                    else:
                        op_2_1 = (a_partner, a)

                    if b < b_partner:
                        op_2_2 = (b, b_partner)
                    else:
                        op_2_2 = (b_partner, b)

                    if op_2_1[0] < op_2_2[0]:
                        op_2 = (op_2_1, op_2_2)
                    else:
                        op_2 = (op_2_2, op_2_1)

                    ordered_operation = (op_1, op_2)
                    return ordered_operation


                elif a_partner in adjacenciesA_copy and (((a, a_partner) in adjacenciesB) or (a_partner, a) in adjacenciesB):
                    operation = ((a_partner, (a, b)), ((a, a_partner), b))

                    #order operation
                    if a<b:
                        op_1_2 = (a, b)
                    else:
                        op_1_2 = (b, a)
                    if a < a_partner:
                        op_2_1 = (a, a_partner)
                    else:
                        op_2_1 = (a_partner, a)
                    ordered_operation = ((a_partner, op_1_2), ((op_2_1), b))
                    return  ordered_operation




                elif b_partner in adjacenciesA_copy and (((b, b_partner) in adjacenciesB) or (b_partner, b) in adjacenciesB):
                    operation = ((b_partner, (a, b)), (((b, b_partner), a)))
                    # order operation
                    if a < b:
                        op_1_2 = (a, b)
                    else:
                        op_1_2 = (b, a)
                    if b < b_partner:
                        op_2_1 = (b, b_partner)
                    else:
                        op_2_1 = (b_partner, b)

                    ordered_operation = ((b_partner, op_1_2), (op_2_1, a))
                    return ordered_operation

                else:
                    return False


        #else if it is a single gene circular chromosome
        else:
            print('THIS IS HAPPENING')
            adjacenciesA_copy = copy.deepcopy(adjacenciesA)

            a = circular_adjacency[0]
            b = circular_adjacency[1]
            if a % 1 == 0:
                a_partner = a - 0.5
            else:
                a_partner = int(a + 0.5)
            if b % 1 == 0:
                b_partner = b - 0.5
            else:
                b_partner = int(b + 0.5)

            if a_partner < b_partner:
                circular_adjacency_partner = (a_partner, b_partner)
            else:
                circular_adjacency_partner = (b_partner, a_partner)

            # if partner is an adjacency
            if circular_adjacency_partner in adjacenciesA_copy:
                operation = ((circular_adjacency, circular_adjacency_partner), ((a, a_partner), (b, b_partner)))
                # order operation
                if circular_adjacency[0] < circular_adjacency_partner[0]:
                    op_1 = (circular_adjacency, circular_adjacency_partner)
                else:
                    op_1 = (circular_adjacency_partner, circular_adjacency)

                if a < a_partner:
                    op_2_1 = (a, a_partner)
                else:
                    op_2_1 = (a_partner, a)

                if b < b_partner:
                    op_2_2 = (b, b_partner)
                else:
                    op_2_2 = (b_partner, b)

                if op_2_1[0] < op_2_2[0]:
                    op_2 = (op_2_1, op_2_2)
                else:
                    op_2 = (op_2_2, op_2_1)

                ordered_operation = (op_1, op_2)
                return ordered_operation


            elif a_partner in adjacenciesA_copy and (
                    ((a, a_partner) in adjacenciesB) or (a_partner, a) in adjacenciesB):
                operation = ((a_partner, (a, b)), ((a, a_partner), b))

                # order operation
                if a < b:
                    op_1_2 = (a, b)
                else:
                    op_1_2 = (b, a)
                if a < a_partner:
                    op_2_1 = (a, a_partner)
                else:
                    op_2_1 = (a_partner, a)
                ordered_operation = ((a_partner, op_1_2), ((op_2_1), b))
                return ordered_operation




            elif b_partner in adjacenciesA_copy and (
                    ((b, b_partner) in adjacenciesB) or (b_partner, b) in adjacenciesB):
                operation = ((b_partner, (a, b)), (((b, b_partner), a)))
                # order operation
                if a < b:
                    op_1_2 = (a, b)
                else:
                    op_1_2 = (b, a)
                if b < b_partner:
                    op_2_1 = (b, b_partner)
                else:
                    op_2_1 = (b_partner, b)

                ordered_operation = ((b_partner, op_1_2), (op_2_1, a))
                return ordered_operation

            else:
                return False

