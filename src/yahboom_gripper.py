from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.gripper import Gripper
from viam.components.arm import Arm
from viam.logging import getLogger

from .yahboom import yahboom
from .controller import YahboomServoController

LOGGER = getLogger(__name__)

class yahboom_gripper(Gripper, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("viamlabs", "gripper"), "yahboom_gripper")

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        LOGGER.info("new gripper")
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        my_class.controller = YahboomServoController()
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        LOGGER.info("new config gripper", config.attributes)
        arm = config.attributes.fields["arm"].string_value
        if arm == "":
            raise Exception("An arm must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # here we initialize the resource instance, the following is just an example and should be updated as needed
        # self.some_pin = int(config.attributes.fields["some_pin"].number_value)
        arm_name = config.attributes.fields["arm"].string_value
        # LOGGER.info("arm name", config.attributes.fields["arm"].string_value, "end")
        arm = dependencies[Arm.get_resource_name(arm_name)]
        self.arm = cast(yahboom, arm)
        LOGGER.info("here")
        return

    """ Implement the methods the Viam RDK defines for the Gripper API (rdk:components:gripper) """

    
    async def open(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        """
        Open the gripper.
        """
        self.controller.write_servo(6, 90, 1000)
        return

    
    async def grab(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> bool:
        """
        Instruct the gripper to grab.

        Returns:
            bool: Indicates if the gripper grabbed something.
        """
        self.controller.write_servo(6, 180, 1000)
        return

    
    async def stop(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        """
        Stop the gripper. It is assumed the gripper stops immediately.
        """
        return

    
    async def is_moving(self) -> bool:
        """
        Get if the gripper is currently moving.

        Returns:
            bool: Whether the gripper is moving.
        """
        pass

