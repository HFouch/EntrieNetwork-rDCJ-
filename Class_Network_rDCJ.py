from Class_rDCJ_Node import Node
import networkx as nx

class Network:

    def __init__(self, start_node, target_node, adjacenciesB):
        self.hash_table = {}
        self.start_node = start_node
        self.target_node = target_node
        self.adjacenciesB = adjacenciesB

        hash_key_start = hash(str(self.start_node.state))
        hash_key_target = hash(str(self.target_node.state))
        self.hash_table.update({hash_key_start: self.start_node})
        self.hash_table.update({hash_key_target: self.target_node})
        self.level = 0

        print('Hash', self.hash_table)

        # Build network

    def build_hash_table(self, current_node):
        node = current_node
        print()
        print('node: ', node)
        print('__________________________')
        print('level: ', self.level)




        if node.next_operation:
            operations = []
            operations.append(node.next_operation)
            operations.append('end')

        else:
            operations = node.get_legal_operations(self.adjacenciesB)
            operations.append('end')

        print('operations: ', operations)

        for operation in operations:
            print()
            print('     operation: ', operation)

            if operation == 'end':
                if self.level ==1:
                    print('RETURNING')
                    print(self.hash_table)
                    print()
                    return self.hash_table
                else:
                    self.level-=1
                    print('     new_level: ', self.level)
                    pass

            else:
                child_state = node.take_action(operation)
                check_hash_table = Network.check_hash_key(self, child_state)

                if check_hash_table[0]:
                    child = check_hash_table[1]
                    print('     child in #T ', child)
                    node.children.append(child)
                    if child != self.target_node:
                        self.level+=1
                    print('     ---> child, level: ', child, self.level)

                else:
                    child = Node(child_state)
                    print('     child not in #T ', child)

                    # check whether a circular chromosome has been created
                    child.find_chromosomes(child.state)

                    # if a circular chromosome has been created:
                    if len(child.circular_chromosomes) != 0:

                        # get legal reinsertion operation
                        for adjacency in operation[-1]:
                            if adjacency in child.circular_chromosomes[0]:
                                circular_join = adjacency
                                potential_operation = child.check_if_operation_exists(circular_join, self.adjacenciesB)
                                #print('legal op: ', potential_operation)

                                # if the a legal operation exists:

                                if potential_operation:
                                    print('     legal op exists')
                                    child.next_operation = potential_operation
                                    hash_key = hash(str(child.state))
                                    self.hash_table.update({hash_key: child})
                                    #print('#T: ', self.hash_table)
                                    node.children.append(child)
                                    self.level+=1
                                    print('     ---> child, level: ', child, self.level)
                                    Network.build_hash_table(self, child)
                                    print()

                                # else if there exists no legal reinsertion operation
                                else:
                                    print('     there was no legal op.. moving on..')
                                    print()
                                    pass

                    # else if no circular chromosome has been created:
                    else:
                        #print('no cicular chrms')
                        hash_key = hash(str(child.state))
                        self.hash_table.update({hash_key: child})
                        #print('#T: ', self.hash_table)
                        node.children.append(child)
                        self.level+=1
                        print('     ---> child, level: ', child, self.level)
                        #print('the children: ', node.children)
                        Network.build_hash_table(self, child)





    def check_hash_key(self, child_state):
        key = hash(str(child_state))
        if key in self.hash_table.keys():
            return True, self.hash_table.get(key)
        return False, None

    def build_network(self):
        network = nx.DiGraph()
        nodes = []
        Network.build_hash_table(self, self.start_node)
        list_of_values = self.hash_table.values()
        for value in list_of_values:
            if value not in nodes:
                nodes.append(value)
        for node in nodes:
            network.add_node(node)
        for node in nodes:
            for child in node.children:
                network.add_edge(node, child)

        return network

    def get_all_shortest_paths(self):
        network = Network.build_network(self)
        all_paths = nx.all_simple_paths(network, self.start_node, self.target_node)
        return all_paths