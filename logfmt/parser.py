# -*- coding: utf-8 -*-
import json.decoder
import enum

class State(enum.Enum):
    GARBAGE = 0
    KEY = 1
    EQUAL = 2

# returns the index after the last character of the ident
def parse_ident(str, start):
    i = start
    while i < len(str):
        c = str[i]
        if c > " " and c != '"' and c != "=":
            i += 1
        else:
            return i
    return i

def parse_line(line):
    json_decoder = json.decoder.JSONDecoder()
    output = {}
    state: State = State.GARBAGE
    i = 0
    value = True

    def conclude():
        nonlocal state, i
        output[key] = value
        state = State.GARBAGE
        i += 1

    while i < len(line):
        c = line[i]
        match state:
            case State.GARBAGE:
                if c > " " and c != '"' and c != "=":
                    m = i
                    i = parse_ident(line, i)
                    key = line[m:i]
                    state = State.KEY
                    value = True
                else:
                    i += 1
            case State.KEY:
                if c == "=":
                    state = State.EQUAL
                    i += 1
                else:
                    conclude()
            case State.EQUAL:
                if c > " " and c != '"' and c != "=":
                    m = i
                    i = parse_ident(line, i)
                    value = line[m:i]
                elif c == '"':
                    value, i = json_decoder.raw_decode(line, idx=i)
                conclude()
    
    if state != State.GARBAGE:
        conclude()
    return output
