"""SMS backends."""

from importlib import import_module

from .. import constants


class SMSBackend:
    """Base class of every SMS backend."""

    serializer_settings: dict = {}
    settings: dict = {}
    structure: list = []
    visibility_rules: dict = {}

    def __init__(self, params):
        """Default constructor."""
        self._params = params

    def send(self, text, recipients):
        """Send a new SMS to given recipients."""
        raise NotImplementedError


def get_backend_class(name):
    """Return class for given backend."""
    backend_module = import_module(f"modoboa.core.sms_backends.{name}")
    try:
        backend_class = getattr(backend_module, f"{name.upper()}Backend")
    except AttributeError:
        return None
    else:
        return backend_class


def get_backend_settings(name):
    """Return settings of given backend."""
    backend_class = get_backend_class(name)
    if not backend_class:
        return None
    return backend_class.settings


def get_backend_serializer_settings(name):
    """Return serializer settings of given backend."""
    backend_class = get_backend_class(name)
    if not backend_class:
        return None
    return backend_class.serializer_settings


def get_all_backend_serializer_settings():
    """Return serializer settings of all backends."""
    settings = {}
    for backend in constants.SMS_BACKENDS:
        name = backend[0]
        if not name:
            continue
        b_settings = get_backend_serializer_settings(name)
        if b_settings:
            settings.update(b_settings)
    return settings


def get_backend_structure(name):
    """Return parameters structure of given backend."""
    backend_class = get_backend_class(name)
    if not backend_class:
        return None
    return backend_class.structure


def get_all_backend_structures():
    """Return parameters structure for all backends."""
    structure = []
    for backend in constants.SMS_BACKENDS:
        name = backend[0]
        if not name:
            continue
        b_structure = get_backend_structure(name)
        if b_structure:
            structure += b_structure
    return structure


def get_active_backend(parameters):
    """Return active SMS backend."""
    name = parameters.get_value("sms_provider")
    if not name:
        return None
    backend_class = get_backend_class(name)
    if not backend_class:
        return None
    return backend_class(parameters)
