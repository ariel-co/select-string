# def Select_String(
#     patterns: list, lines: typing.Iterable,
#     precontext:int = 0, postcontext:int = 0, flags:int = 0, self.simplematch:bool = False,
#     self.allmatches: bool=False
# ) -> typing.Iterable:
# 
#     from collections import deque  # for precontext
# 
#     _patterns = [ re.compile(pat) if pat is str and not self.simplematch else pat for pat in patterns ]
#     
#     _precontext = deque([], maxlen=precontext)
# 
#     for line in lines:
#         matches = _matches(_patterns, line, self.allmatches)
#         yield line
#         _precontext.append(line)
# 

## TODO --overlap-contexts

from pprint import pprint
