from transitions import Machine 
from transitions.extensions import HierarchicalGraphMachine as Machine


class robot(object):
    pass 


states = ['idle', 'begin', {'name': 'driving', 'children': ['forward', 'reversing',
          'turn_left', 'turn_right', 'stop']}, 'off',
          {'name': 'picking', 'children': ['arm_up', 'arm_down', 'rotate']},
          {'name': 'conversation', 'initial': 'wait_for_message', 'children': ['wait_for_message', 'process', 'answer', 'answer_error']},
          ]

# transitions = [trigger, source, destination]
transitions = [['power', 'off', 'idle'],
               ['pyrosense', 'idle', 'begin'],
               ['error', 'idle', 'idle'],
               ['vc_drive', 'begin', 'driving'],
               ['vc_stop', ['driving_forward', 'driving_turn_right', 'driving_turn_left', 'driving_reversing'], 'driving_stop'],
               ['', 'driving_turn_left', 'driving_forward'],
               ['', 'driving_reversing', 'driving_forward'],
               ['', 'driving_turn_right', 'driving_forward'],
               ['', 'driving_turn_left', 'driving_reversing'],
               ['', 'driving_turn_right', 'driving_reversing'],
               ['sense_is_', 'driving_forward', 'driving_reversing'],
               ['', 'driving_forward', 'driving_forward'],
               ['', 'driving_reversing', 'driving_reversing'],
               ['', 'driving_forward', 'driving_turn_right'],
               ['', 'driving_forward', 'driving_turn_left'],
               ['', 'driving_reversing', 'driving_turn_left'],
               ['', 'driving_reversing', 'driving_turn_right'],
               ['vc_is_hei', 'begin', 'conversation'],
               ['receive_voice_message', 'conversation_wait_for_message', 'conversation_process'],
               ['error', 'conversation_process', 'conversation_answer_error'],
               ['answer_ready', 'conversation_process', 'conversation_answer'],
               ['', 'conversation_answer', 'conversation_wait_for_message'],
               ['', 'conversation_answer_error', 'conversation_wait_for_message'],
               ['', 'begin', 'picking']
               ]

Cogitron = robot()
machine = Machine(model=Cogitron, use_pygraphviz=False, states=states, transitions=transitions, initial='off')

Cogitron.power()
Cogitron.pyrosense()

Cogitron.get_graph().draw('my_state_diagram.png', prog='dot')