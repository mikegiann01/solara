import traceback
from typing import Any, Dict

try:
    import comm
except ImportError:
    comm = None

orphan_comm_stacks: Dict[Any, str] = {}
if comm is not None:

    class DummyComm(comm.base_comm.BaseComm):  # type: ignore
        def publish_msg(self, msg_type, data=None, metadata=None, buffers=None, **keys):
            pass

    def create_dummy_comm(*args, **kwargs):
        comm = DummyComm(*args, **kwargs)
        stacktrace = "".join(traceback.format_stack())
        orphan_comm_stacks[comm] = stacktrace
        return comm

    comm.create_comm = create_dummy_comm
else:

    class DummyComm:  # type: ignore
        pass
