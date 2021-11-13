import re
import typing
from dataclasses import dataclass
from enum import IntEnum, unique
from warnings import warn

@unique
class PatternLogic(IntEnum):
    ANY = 0   # 
    ALL = 1
    # NONE = 2 # the caller can negate ANY
    
globals().update(PatternLogic.__members__)
_logic = PatternLogic

# `Select-String` consumes the first pattern that matches:
# 
#     > "abcdef" | select-string ..,... -AllMatches | select -exp matches | select -exp value
#     ab
#     cd
#     ef
#     > "abcdef" | select-string ....,... -AllMatches | select -exp matches | select -exp value
#     abcd
#     > "abcdef" | select-string cd,abc -AllMatches | select -exp matches | select -exp value
#     cd
# 
# In `grep`, the longest pattern matches first and consumes:
# 
#     $ echo abcdef | grep -o -e .. -e ....
#     abcd
#     ef
#     $ echo abcdef | grep -o -e ab -e bcd
#     ab
@unique
class PatternPriority(IntEnum):
    IN_ORDER = 0       # PowerShell style
    LONGEST_FIRST = 1  # grep style
    
globals().update(PatternPriority.__members__)
_prio = PatternPriority

# TODO
# class Match
#     Value should be a computed property instead of a str

@dataclass(frozen=True)
class LineMatcher:
    patterns:typing.List[str]
    simplematch:bool = False  #
    ignorecase:bool  = False  #
    allmatches:bool  = False  # scan the whole string for matches
    patternlogic:PatternLogic = _logic.ANY # string must match any/all/no patterns
    patternpriority:PatternPriority = _prio.IN_ORDER
    _patterns:typing.List = [] # internal # TODO hide field?

    def __post_init__(self) -> typing.List: # TODO [Match]
        if self.patternpriority != _prio.IN_ORDER:
            warn(f"{self.patternpriority} not implemented yet")
        for pat in self.patterns:
            if isinstance(pat,str):
                if self.simplematch:
                    _pat = pat.lower() if self.ignorecase else pat
                else:
                    _pat = re.compile(pat, flags = re.I if self.ignorecase else 0)
            else:
                _pat = pat
        self._patterns.append(_pat)

    """ Returns generator of non-overlapping matches for a line """    
    def _matches_inorder(self, line:str): # TODO -> Generator[??]
        offset = 0
        _line = line.lower() if self.simplematch and self.ignorecase else line

        while offset < len(line):
            for idx,pat in enumerate(self._patterns):
                if self.simplematch:
                    pos = line.find(pat,offset)
                    if pos > -1:
                        yield (line[pos:pos+len(pat)], pos, self.patterns[idx])
                        offset = pos + len(pat)
                else:
                    match = pat.search(line, offset)
                    if match:
                        yield (match, self.patterns[idx])
                        offset = match.end()

    _matches = _matches_inorder  # TODO

    def matches(self, line:str):
        matcher = self._matches(line)

        if self.patternlogic == _logic.ANY:
            firstmatch = next(matcher)
            if firstmatch:
                yield firstmatch
                if self.allmatches:
                    yield from matcher
            else:
                return
        elif self.patternlogic == _logic.ALL:
             ##×× matchers = [ _matches(p) for p in self._patterns ]
            pass

# from pprint import pprint
# pprint(
#     _matches( ["ab","bc","cd","xx"], "abcdeabcde", self.allmatches=True, self.simplematch=True )
# )
# pprint(
#     _matches( [re.compile("ab"),re.compile("bc"),re.compile("cd"),re.compile("xx")], "abcdeabcde", self.allmatches=True # )
# )
# 


