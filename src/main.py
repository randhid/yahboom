"""
This module implements a yahboom dofbot arm for integration 
and control through Viam.
"""
import asyncio

from viam.components.arm import Arm
from viam.components.gripper import Gripper
from viam.module.module import Module

from viam.components.arm import Arm
from viam.components.gripper import Gripper
from viam.resource.registry import Registry, ResourceCreatorRegistration

from yahboom_arm import yahboom_arm
from yahboom_gripper import yahboom_gripper


async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
    Args:
        address (str): The address to serve the module on
    """

    Registry.register_resource_creator(
    Arm.SUBTYPE, yahboom.MODEL,
    ResourceCreatorRegistration(yahboom.new, yahboom.validate)
    )
    
    Registry.register_resource_creator(
    Gripper.SUBTYPE,
    yahboom_gripper.MODEL,
    ResourceCreatorRegistration(yahboom_gripper.new, yahboom_gripper.validate
    ))

    module = Module.from_args()
    module.add_model_from_registry(Arm.SUBTYPE, yahboom.MODEL)
    module.add_model_from_registry(Gripper.SUBTYPE, yahboom_gripper.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
