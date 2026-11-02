class WorkflowError(Exception):
    """A safe, actionable workflow failure."""


class ConfigurationError(WorkflowError):
    pass


class GateError(WorkflowError):
    pass


class LockError(WorkflowError):
    pass
