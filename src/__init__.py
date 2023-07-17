"""
This file registers the model with the Python SDK.
"""

from viam.components.arm import Arm
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .yahboom import yahboom

Registry.register_resource_creator(Arm.SUBTYPE, yahboom.MODEL, ResourceCreatorRegistration(yahboom.new, yahboom.validate))
