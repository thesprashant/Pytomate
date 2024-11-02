LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_EXEC = 3
OP_NODE_RESULT = 4
OP_NODE_NOTE = 5
OP_NODE_CHECK = 6
OP_NODE_CODE = 7

TOOL_NODES = {
}

class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in TOOL_NODES:
        raise InvalidNodeRegistration("Duplicite node registration of '%s'. There is already %s" %(
            op_code, TOOL_NODES[op_code]
        ))
    TOOL_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in TOOL_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return TOOL_NODES[op_code]

from elements import *