from numpy.random import randint
from time import sleep
from copy import deepcopy

class Node:
    def __init__(self, name: str, pos: int, start: int, max_wait: int, frames: int) -> None:
        self.name = name
        self.pos = pos
        self.wait = start
        self.max_wait = max_wait
        self.frames = frames

        self.collision = False
        self.collision_count = 0
        self.transmitting = False

        self.total_collisions = 0
        self.total_waiting = 0

    def __str__(self) -> str:
        if self.transmitting:
            if self.collision:
                return "Kolizja"
            else:
                return "Aktywny"
        else:
            if self.frames == 0:
                return "Nieaktywny"
            else:
                return "Oczekiwanie"
    
    def Wait(self) -> None:
        self.collision_count += 1
        self.wait = randint(0, self.max_wait + 1)
        self.total_waiting += self.wait

class Signal:
    def __init__(self, node: Node, dir: int) -> None:
        self.node = node
        self.dir = dir
        self.jam = node.collision
    
    def __str__(self) -> str:
        if self.jam:
            return self.node.name[0] + "*"
        return self.node.name[0]
    
class Sim:
    def __init__(self, size: int) -> None:
        self.nodes = [None for _ in range(size)]
        self.active_nodes = []
        self.cable = [[] for _ in range(size)]
        self.empty_cable = [[] for _ in range(size)]

        self.size = size

        self.names = ["" for _ in range(size)]
    
    def addNode(self, name: str, pos: int, start: int, max_wait: int, frames: int) -> None:
        node = Node(name, pos, start, max_wait, frames)
        if pos < self.size:
            self.nodes[pos] = node
            self.names[pos] = name
            if frames > 0:
                self.active_nodes.append(node)
        else:
            raise Exception(f"Pozycja musi być pomiędzy 0 a {self.size - 1}")
    
    def execute(self) -> None:
        i = -1
        while self.active_nodes or self.cable != self.empty_cable:
            i += 1
            self.timeFrame()
            self.printState()
            sleep(1)
        
        print(f"\n\nWyniki symulacji:\n{i} iteracji\n")
        print(f"{'Nazwa':<12}{'Kolizje':<12}Czas czekania")
        for node in self.nodes:
            if node:
                print(f"{node.name:<12}{node.total_collisions:<12}{node.total_waiting:<12}")

    def timeFrame(self) -> None:
        next_cable = deepcopy(self.empty_cable)
        for i, segment in enumerate(self.cable):
            for signal in segment:
                if signal.dir == 0:
                    if i > 0:
                        next_cable[i - 1].append(Signal(signal.node, -1))
                    if i + 1 < self.size:
                        next_cable[i + 1].append(Signal(signal.node, +1))
                elif i + signal.dir in range(max(0, i + signal.dir), min(self.size, i + signal.dir + 1)):
                    next_cable[i + signal.dir].append(signal)
        
        self.cable = next_cable

        for node in self.active_nodes:
            if not node.transmitting:
                if node.wait == 0:
                    if not self.cable[node.pos]:
                        self.cable[node.pos].append(Signal(node, 0))
                        node.transmitting = True
                        node.wait = self.size * 2 - 2
                    else:
                        node.total_waiting += 1
                else:
                    node.wait -= 1
            else:
                if node.wait == 0:
                    node.transmitting = False

                    if node.collision:
                        node.collision = False
                        node.Wait()
                    else:
                        node.frames -= 1
                        node.total_collisions += node.collision_count
                        node.collision_count = 0
                        if node.frames == 0:
                            self.active_nodes.remove(node)
                else:
                    if not node.collision and len(self.cable[node.pos]) > 0:
                        node.collision = True
                        node.wait = self.size * 2 - 2
                    self.cable[node.pos].append(Signal(node, 0))
                    node.wait -= 1
    
    def printState(self) -> None:
        wait_times = ["" for _ in range(self.size)]
        node_states = ["" for _ in range(self.size)]
        for node in self.nodes:
            if node:
                wait_times[node.pos] = node.wait
                node_states[node.pos] = str(node)
        
        print("\n" + "+" + "-" * 7 + "+" + ("-" * 11 + "+") * self.size)

        print(f"|{'Nazwa':^7}|", end="")
        for data in self.names:
            print(f"{data:^11}|", end="")
        print(f"\n|{'Czeka':^7}|", end="")
        for data in wait_times:
            print(f"{data:^11}|", end="")
        print(f"\n|{'Stan':^7}|", end="")
        for data in node_states:
            print(f"{data:^11}|", end="")
        
        print("\n" + "+" + "-" * 7 + "+" + ("-" * 11 + "+") * self.size)

        print(f"|{'Kabel':^7}|", end="")
        signals = [", ".join(str(signal) for signal in segment) for segment in self.cable]
        for segment in signals:
            print(f"{segment:^11}|", end="")
        
        print("\n" + "+" + "-" * 7 + "+" + ("-" * 11 + "+") * self.size)


if __name__ == "__main__":
    sim = Sim(5)
    sim.addNode("A", 0, 0, 20, 2)
    sim.addNode("B", 2, 1, 20, 1)
    sim.addNode("C", 4, 3, 20, 2)
    sim.execute()