import json
import numpy as np
import sympy as sp
import sympy.physics.quantum as spq

def cytoscapeExport(state_system):
    elements = {}
    elements["states"] = []
    elements["correlations"] = []
    for i in state_system.states:
        # set precision to avoid awkward -zeros
        s = []
        for state in state_system.states[i].value:
            s.append(np.around(state, decimals=3))

        measured = ""
        if state_system.states[i].measured:
            measured = "[M]"

        lbl = (
            str(state_system.states[i].uid)
            + "  ["
            + str(state_system.states[i].qudit)
            + "]  "
            + str(np.around(s, 3))
            + " "
            + measured
        )
        nn = {}
        nn["data"] = {}
        nn["data"]["id"] = lbl

        if state_system.states[i].correlation_uid is not None:
            euid = state_system.states[i].correlation_uid
            l_euid = euid + "  " + str(np.around(state_system.correlations[euid].weight, 3))
            nn["data"]["parent"] = l_euid

        elements["states"].append(nn)

    print(json.dumps(elements))

# Transforms the full system
def toStateVector(self):
    pass

#TODO how to use this for qudits in general?
def simplifiedState(state_system, state):
    pass

def printState(state, subs=[]):
    #TODO
    print(state.value)

def printStateSystem(state_system, subs=[]):
    print("      ".join(str(ql) for ql in state_system.quditLabels))
    print("------".join("--" for ql in state_system.quditLabels))  
    phelper = []
    
    for e in state_system.correlations:
        phelper = []
        for ql in state_system.quditLabels:
            nid = state_system.getQuditStateInCorrelation(ql,e)

            if (nid is not None):
                replaced = ' '
                if (state_system.states[nid].replaced):
                    replaced = '*'

                state = state_system.states[nid].value
                for sub in subs:
                    if (sp.symbols(sub) in state.free_symbols):
                        state = state.subs(sp.symbols(sub),subs[sub])

                if (state_system.states[nid].measured):
                    phelper.append(str(state) + ' M')
                else:
                    phelper.append(state)
            else:
                phelper.append("N/A")
        
        if (len(phelper) != 0):
            amp = state_system.correlations[e].weight
            for sub in subs:
                if (sp.symbols(sub) in amp.free_symbols):
                    amp = amp.subs(sp.symbols(sub),subs[sub])

            phelper.append("weight: "+str(amp))

        print("     ".join(str(x) for x in phelper))
    
    print("      ".join("  " for ql in state_system.quditLabels))
    #print(state_system.toStateVector())
    print("------".join("--" for ql in state_system.quditLabels))
    print("      ".join("  " for ql in state_system.quditLabels))
    print("      ".join("  " for ql in state_system.quditLabels))