import asyncio
import sys

from viam.components.arm import Arm
from viam.components.gripper import Gripper
from viam.module.module import Module
from .yahboom import yahboom
from .yahboom_gripper import yahboom_gripper

async def main(address: str):
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
    Args:
        address (str): The address to serve the module on
    """
    module = Module(address)
    module.add_model_from_registry(Arm.SUBTYPE, yahboom.MODEL)
    module.add_model_from_registry(Gripper.SUBTYPE, yahboom_gripper.MODEL)
    await module.start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Need socket path as command line argument")

    asyncio.run(main(sys.argv[1]))
    
