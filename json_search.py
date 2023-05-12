# -*- coding: utf-8 -*-
import json


#----配列などが含まれるjsonから特定のキーを持つ値を取得
#----return list
class JsonSearch:

    def __init__(self, search_key):
        self.search_key = search_key

    def search(self, arg, cond):
        res =[]
        if cond(arg):
            res.append(arg)
        if isinstance(arg, list):
            for item in arg:
                res += self.search(item, cond)
        elif isinstance(arg, dict):
            for value in arg.values():
                res += self.search(value, cond)
        return res

    def has_star_key(self, arg):
        if isinstance(arg, dict):
            #ここで調整
            return self.search_key in arg.keys()

    def get_star(self, arg):
        return self.search(arg, self.has_star_key)


if __name__ == "__main__":
    jse = JsonSearch(search_key="id_str")
