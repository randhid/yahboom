"""
This file registers the model with the Python SDK.
"""

from viam.components.arm import Arm
from viam.components.gripper import Gripper
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .yahboom import yahboom
from .yahboom_gripper import yahboom_gripper

Registry.register_resource_creator(
    Arm.SUBTYPE, yahboom.MODEL,
    ResourceCreatorRegistration(yahboom.new, yahboom.validate)
    )
Registry.register_resource_creator(
    Gripper.SUBTYPE,
    yahboom_gripper.MODEL,
    ResourceCreatorRegistration(yahboom_gripper.new, yahboom_gripper.validate
    ))
