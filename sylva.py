import os
import json
from typing import List, Dict
from collections import UserDict, namedtuple, UserList

class Sylva(UserList):
    sylva_path = "./sylva.json"

    def __setattr__(self, name: str, value: list) -> None:
        try:
            if name == 'data':
                super().__setattr__(name, value)
            else:
                for item in self.data:
                    if item['name'] == name:
                        item['data'] = value
                        return
                self.data.append({'name': name, 'data': value})
        except Exception as e:
            raise AttributeError(f"Error setting attribute {name}: {e}")
    
    def __getattr__(self, name: str) -> list:
        try:
            for item in self.data:
                if item['name'] == name:
                    return item['data']
            raise AttributeError(f"No such attribute: {name}")
        except KeyError as e:
            raise AttributeError(f"Error getting attribute {name}: {e}")
        
    def find(self, name: str):
        for item in self.data:
            if item['name'] == name:
                return item['data']
        return None
        
    def load(self) -> None:
        if not os.path.exists(Sylva.sylva_path):
            with open(Sylva.sylva_path, 'w') as f:
                json.dump([], f)
        with open(Sylva.sylva_path, 'r') as f:
            self.data = json.load(f)

    def save(self) -> None:
        with open(Sylva.sylva_path, 'w') as f:
            json.dump(self.data, f, indent=4)

# retieve data from database and give a inferface to access it
class NamedDict(UserDict):
    def __init__(self, **kwargs):
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in self._fields()}
        super().__init__(filtered_kwargs)
        for key in self._fields():
            if key not in self.data:
                self.data[key] = None

    def _fields(self):
        raise NotImplementedError
    
    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key in self._fields():
            self.data[key] = value
        else:
            super().__setattr__(key, value)

    def to_dict(self):
        return dict(self.data)
    
    def to_space(self):
        for key in self._fields():
            if self.data[key] is None:
                self.data[key] = ''
        return self
    
FolderData = lambda folder_name: ArticleData(title=folder_name)
    
class ArticleData(NamedDict):
    def _fields(self):
        return ['title', 'author', 'journal', 'year', 'doi', 'local_path', 'add_time']
    
class NoteData(NamedDict):
    def _fields(self):
        return ['title', 'note', 'add_time', 'changed_time', 'quote', 'torder']
    
class AnnotationData(NamedDict):
    def _fields(self):
        return ['annot', 'refer', 'page_number', 'add_time', 'changed_time', 'colour', 'torder']

                         