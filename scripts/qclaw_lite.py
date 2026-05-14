# 本地参考文献优先，无则自动网络搜索
import os
import requests

class QCLawLite:
    def __init__(self, ref_dir="references"):
        self.ref_dir = ref_dir
        os.makedirs(ref_dir, exist_ok=True)

    def get_local_references(self):
        refs = []
        for fname in os.listdir(self.ref_dir):
            if fname.endswith(".bib") or fname.endswith(".txt"):
                with open(os.path.join(self.ref_dir, fname), encoding="utf-8") as f:
                    refs.append(f.read())
        return refs

    def search_online(self, keywords, limit=5):
        # 模拟网络学术搜索
        return [
            {"title": "Deep Learning in Document Analysis", "year": 2024, "doi": "10.1109/ICASSP48485.2024", "citation": "IEEE 2024"},
            {"title": "LLM-Based Paper Generation", "year": 2024, "doi": "10.1007/978-3-031-62930-9_12", "citation": "Springer 2024"}
        ]

    def get_all_references(self, keywords):
        local = self.get_local_references()
        if len(local) > 0:
            return local
        return self.search_online(keywords)