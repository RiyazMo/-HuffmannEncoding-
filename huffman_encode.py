import networkx as nx
from collections import Counter

class HuffmanEncoding():

    @staticmethod
    def frequency(msg : str) -> dict:
        if len(msg) > 1:
            return sorted(Counter(msg).items(), key = lambda x : x[1])
        else:
            return None
        
    @classmethod
    def from_txt(self, path:str) -> HuffmanEncoding:
        with open(path, mode = "r") as f:
            HE = HuffmanEncoding(f.read())
            f.close()
        return HE
            
    def __init__(self, msg : str):
        self._msg = msg
        self._freq = HuffmanEncoding.frequency(msg)
        self._tree = self._build_huffman_tree()
        self._enc_table = self._compute_encoding_table() 
    
    @property
    def huffman_tree(self) -> dict:
        return self._tree   
    
    @property
    def freq(self) -> dict:
        return self._freq 
    
    @property
    def msg(self) -> dict:
        return self._msg 
    
    def _build_child_tree(self, node, child_node_0 : str, child_note_0_freq: int, child_node_1: str, child_note_1_freq: int,
             child_note_0_bit = 0, child_note_1_bit = 1) -> nx:
        DG = nx.DiGraph([(node, child_node_0), (node, child_node_1)])
        child_attr =  {node: {'bit': 1, "freq": child_note_0_freq + child_note_1_freq},
                       child_node_0: {"bit": child_note_0_bit, "freq": child_note_0_freq},
                       child_node_1: {"bit": child_note_1_bit, "freq": child_note_1_freq}}
        nx.set_node_attributes(DG, child_attr)
        return DG

    def _build_huffman_tree(self) -> nx:
        n = len(self._freq)
        if n < 2:
            return []
        freq_s = self._freq.copy()
        right_child = freq_s.pop(0)
        left_child = freq_s.pop(0)
        sub_graph_root_name = n - 1 #right_child[0] + left_child[0]
        sub_graph_root_freq = right_child[1] + left_child[1]
        DG = self._build_child_tree(sub_graph_root_name, right_child[0], right_child[1],
                                left_child[0], left_child[1])
        for elem in freq_s:
            curr_node_name, curr_node_freq = elem
            DG.add_edges_from([(sub_graph_root_name - 1, curr_node_name), 
                               (sub_graph_root_name - 1, sub_graph_root_name)])
            sub_graph_root_freq = sub_graph_root_freq + curr_node_freq
            sub_graph_root_name = sub_graph_root_name - 1
            pos = {curr_node_name: {'bit': 0, 'freq': curr_node_freq},
                   sub_graph_root_name: {'bit': 1, 'freq': sub_graph_root_freq}
                  }
            nx.set_node_attributes(DG, pos)
        return DG
    
    @property
    def encoding_table(self) -> dict:
        return self._enc_table
    
    def _compute_encoding_table(self) -> dict:
        res_d = {}
        for letter, _ in self._freq:
            res = ""
            i = 1
            while letter not in list(self._tree.successors(i)):
                res += "1"
                i += 1
            res += str(self._tree.nodes[letter]["bit"])
            res_d[letter] = res
        return res_d
    
    def encode(self) -> str:
        enc_tbl = self.encoding_table
        res = ""
        for character in self._msg:
            res += enc_tbl[character]
        return res
    
    
    def decode(self, bits) -> str:
        j = 2
        nodes = list(self._tree.successors(1))
        res = ""
        for i in range(len(bits)):
            if bits[i] == "0":
                res += nodes[0]
                nodes = list(self._tree.successors(1))
                j = 1
            elif bits[i] == "1" and j == len(self._freq):
                res += nodes[1]
                nodes = list(self._tree.successors(1))
                j = 1
            else:
                nodes = list(self._tree.successors(j))
            j += 1
        return res

if __name__ == "__main__":
    print("Text:")
    s = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
    HE = HuffmanEncoding(s)
    bits = HE.encode()
    s_d = HE.decode(bits)
    print(s)
    print(s_d)
    print("equal:", s_d == s)

    print("From file:")
    path = r"to_compress.txt"
    HE = HuffmanEncoding.from_txt(path)
    bits = HE.encode()
    msg = HE.decode(bits)
    with open(path, "r") as f:
        txt = f.read()
        f.close()
    print("equal:", txt == msg)
    
