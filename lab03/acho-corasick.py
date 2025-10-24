from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

@dataclass
class ACNode:
    next: Dict[str, int] = field(default_factory=dict)   
    fail: int = 0                                        
    out: List[int] = field(default_factory=list)         


class AhoCorasick:
    def __init__(self, ignore_case: bool = False):
        self.ignore_case = ignore_case
        self.nodes: List[ACNode] = [ACNode()] 
        self.patterns: List[str] = []

    def _norm(self, s: str) -> str:
        return s.lower() if self.ignore_case else s

    def add_pattern(self, pattern: str) -> None:

        if not pattern:
            return
        pat = self._norm(pattern)
        cur = 0
        for ch in pat:
            if ch not in self.nodes[cur].next:
                self.nodes[cur].next[ch] = len(self.nodes)
                self.nodes.append(ACNode())
            cur = self.nodes[cur].next[ch]
        self.nodes[cur].out.append(len(self.patterns))
        self.patterns.append(pattern) 

    def add_patterns(self, patterns: List[str]) -> None:
        for p in patterns:
            self.add_pattern(p)

    def build(self) -> None:
        q = deque()
        for ch, nxt in self.nodes[0].next.items():
            self.nodes[nxt].fail = 0
            q.append(nxt)
        while q:
            v = q.popleft()
            for ch, u in self.nodes[v].next.items():
                q.append(u)
                f = self.nodes[v].fail
                while f != 0 and ch not in self.nodes[f].next:
                    f = self.nodes[f].fail
                if ch in self.nodes[f].next:
                    f = self.nodes[f].next[ch]
                self.nodes[u].fail = f
                self.nodes[u].out.extend(self.nodes[f].out)

    def search(self, text: str) -> List[Tuple[int, int, int, str]]:
        norm_text = self._norm(text)
        res: List[Tuple[int, int, int, str]] = []
        v = 0
        for i, ch in enumerate(norm_text):
            while v != 0 and ch not in self.nodes[v].next:
                v = self.nodes[v].fail
            if ch in self.nodes[v].next:
                v = self.nodes[v].next[ch]
            if self.nodes[v].out:
                for pid in self.nodes[v].out:
                    pat = self._norm(self.patterns[pid])
                    start = i - len(pat) + 1
                    end = i
                    res.append((start, end, pid, self.patterns[pid]))
        return res

if __name__ == "__main__":
    ac = AhoCorasick(ignore_case=True)
    ac.add_patterns(["ala", "Ala ma", "ma", "lama"])
    ac.build()

    text = "Ala ma kota, a lama ma alalalę."
    matches = ac.search(text)

    for start, end, pid, pat in matches:
        fragment = text[start:end+1]
        print(f"{pat!r} @ [{start},{end}] -> '{fragment}'")
