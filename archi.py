import os
import json
from typing import List, Dict
from collections import UserDict, namedtuple, UserList

class Archi(UserList):
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
        if not os.path.exists('archi.json'):
            with open('archi.json', 'w') as file:
                json.dump([], file)
        with open('archi.json', 'r') as file:
            self.data = json.load(file)

    def save(self) -> None:
        with open('archi.json', 'w') as file:
            json.dump(self.data, file, indent=4)

ProfileData = namedtuple(
    'ProfileData', ['title', 'year', 'journal', 'author', 'add_time', 'rank']
    )

ProfileNote = namedtuple(
    'ProfileNote', ['title', 'note', 'date', 'torder']
    )

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
    
class ArticleData(NamedDict):
    def _fields(self):
        return ['title', 'author', 'journal', 'year', 'doi', 'local_path', 'add_time']
    
class NoteData(NamedDict):
    def _fields(self):
        return ['title', 'note', 'date', 'related_content', 'torder']
    
class AnnotationData(NamedDict):
    def _fields(self):
        return ['annot', 'date', 'page_number', 'quote_content', 'colour', 'torder']

                         