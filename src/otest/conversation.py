import json
import logging
from otest import Trace
from otest.interaction import Interaction
from otest.events import Events

__author__ = 'roland'

logger = logging.getLogger(__name__)



class Conversation(object):
    def __init__(self, flow, entity, msg_factory, check_factory=None,
                 features=None, trace_cls=Trace, interaction=None, opid=None,
                 **extra_args):
        self.flow = flow
        self.entity = entity
        self.msg_factory = msg_factory
        self.trace = trace_cls(True)
        self.events = Events()
        self.interaction = Interaction(self.entity, interaction)
        self.check_factory = check_factory
        self.features = features
        self.operator_id = opid
        self.extra_args = extra_args
        self.test_id = ""
        self.info = {}
        self.index = 0
        self.comhandler = None
        self.exception = None
        self.sequence = []
        self.trace.info('Conversation initiated')
        self.cache = {}

    def dump_state(self, filename):
        state = {
            "client": {
                "behaviour": self.entity.behaviour,
                "keyjar": self.entity.keyjar.dump(),
                "provider_info": self.entity.provider_info.to_json(),
                "client_id": self.entity.client_id,
                "client_secret": self.entity.client_secret,
            },
            "trace_log": {"start": self.trace.start, "trace": self.trace.trace},
            "sequence": self.flow,
            "flow_index": self.index,
            "client_config": self.entity.conf,
            "condition": self.events.get('condition')
        }

        try:
            state["client"][
                "registration_resp"] = \
                self.entity.registration_response.to_json()
        except AttributeError:
            pass

        txt = json.dumps(state)
        _fh = open(filename, "w")
        _fh.write(txt)
        _fh.close()
