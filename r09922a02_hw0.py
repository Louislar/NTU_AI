import sys
from itertools import compress

class Solution:
    def __init__(self):
        self.N = None
        self.M = None
        self.bridges = None
        self.islands = None
        self.route = None
        self.route_num = None
    #Feel free to define your own member function
    class Island: 
        def __init__(self) -> None:
            self.is_empty = False
            # Store the index of island, which is number of island - 1
            self.adjacency = [] 

    def std_input(self): 
        # for line in sys.stdin: 
        #     print(line.rstrip())
        def _parse_one_line_input(str_in): 
            split_in_str = [int(i) for i in str_in.split()]
            return split_in_str[0], split_in_str[1]

        self.N, self.M = _parse_one_line_input(input())
        self.bridges = []
        for i in range(self.M): 
            tmp_island1, tmp_island2 = _parse_one_line_input(input())
            self.bridges.append([tmp_island1, tmp_island2])
        # Test
        # print("input N: ", self.N)
        # print("input M: ", self.M)
        # print('input bridges: ')
        # for i in range(self.M): 
        #     print(self.bridges[i])

    def construct_islands(self): 
        self.islands = [self.Island() for i in range(self.N)]
        for bridge_pair in self.bridges: 
            self.islands[bridge_pair[0]-1].adjacency.append(bridge_pair[1]-1)
            self.islands[bridge_pair[1]-1].adjacency.append(bridge_pair[0]-1)
        for _island in self.islands: 
            _island.adjacency.sort()
            # print(_island.adjacency)

    def plan_the_route(self): 
        # Start with the first island
        self.route = [0]
        self.islands[0].is_empty = True
        # Search for the next adjacency island, which still have grass and smallest index
        while True: 
            tmp_adjacency_idx = self.islands[self.route[-1]].adjacency
            # Terminate when no adjacency island
            if not tmp_adjacency_idx: 
                break
            tmp_adjacency_is_grass_empty = [not self.islands[i].is_empty for i in tmp_adjacency_idx]
            tmp_adjacency_grass_idx = [i for i in compress(tmp_adjacency_idx, tmp_adjacency_is_grass_empty)]
            
            # Test
            # print('======= Cur island {0} ======='.format(self.route[-1]))
            # print('Adjacency: ', tmp_adjacency_idx)
            # print(tmp_adjacency_is_grass_empty)
            # print('Adjacency with grass: ', tmp_adjacency_grass_idx)

            # Terminate when no Island with grass can reach
            if not tmp_adjacency_grass_idx: 
                break
            # Add next island to the route, and the grass on it is empty
            self.route.append(tmp_adjacency_grass_idx[0])
            self.islands[tmp_adjacency_grass_idx[0]].is_empty = True

        # Finally change the route from index to the actual dangerous number of islands in string
        self.route_num = [str(i+1) for i in self.route]
    
    def print_final_route(self): 
        print(' '.join(self.route_num))

    def solve(self):
        self.std_input()
        self.construct_islands()
        self.plan_the_route()
        self.print_final_route()

if __name__ == '__main__':
    ans = Solution()
    ans.solve()