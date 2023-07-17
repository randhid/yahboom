from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast, Tuple
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.arm import Arm, Pose, JointPositions, KinematicsFileFormat
from viam.components.board import Board
from viam.logging import getLogger

from smbus2 import SMBus
import time
import asyncio
import json

LOGGER = getLogger(__name__)

class yahboom(Arm, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("viamlabs", "arm"), "yahboom")
    
    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    bus = SMBus(1)
    addr = 0x15
    joint_positions = None

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        # here we validate config, the following is just an example and should be updated as needed
        board_name = config.attributes.fields["board"].string_value
        if board_name == "":
            raise Exception("A board component is required")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        return

    """ Implement the methods the Viam RDK defines for the Arm API (rdk:components:arm) """

    
    async def get_end_position(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Pose:
        """
        Get the current position of the end of the arm expressed as a Pose.

        Returns:
            Pose: The location and orientation of the arm described as a Pose.
        """
        pass

    
    async def move_to_position(
        self,
        pose: Pose,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        """
        Move the end of the arm to the Pose specified in ``pose``.

        Args:
            pose (Pose): The destination Pose for the arm.
        """
        pass

    
    async def move_to_joint_positions(
        self,
        positions: JointPositions,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        """
        Move each joint on the arm to the corresponding angle specified in ``positions``.

        Args:
            positions (JointPositions): The destination ``JointPositions`` for the arm.
        """
        LOGGER.info(f'moving to positions {positions.values}')
        max_time = 1000
        for i, val in enumerate(positions.values):
            # approx 10 deg per second
            max_time = max(max_time, (abs(val - self.joint_positions[i])*1000//10))
        try:
            await self.write_all_servos(positions, int(max_time))
        except Exception as e:
            LOGGER.error(f'error writing positions {positions.values} to servos')
    
    async def get_joint_positions(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> JointPositions:
        """
        Get the JointPositions representing the current position of the arm.

        Returns:
            JointPositions: The current JointPositions for the arm. [base spin, joint 1, 2, 3, top claw spin]
        """
        values = []
        for id in range(1, 6):
            val = await self.read_servo(id)
            values.append(val)
        # LOGGER.debug(f"joint values log: {values}")
        self.joint_positions = values
        return JointPositions(values=values)

    
    async def stop(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        """
        Stop all motion of the arm. It is assumed that the arm stops immediately.
        """
        pass

    
    async def is_moving(self) -> bool:
        """
        Get if the arm is currently moving.

        Returns:
            bool: Whether the arm is moving.
        """
        pass

    
    async def get_kinematics(self, *, timeout: Optional[float] = None) -> Tuple[KinematicsFileFormat.ValueType, bytes]:
        """
        Get the kinematics information associated with the arm.

        Returns:
            Tuple[KinematicsFileFormat.ValueType, bytes]:
                - KinematicsFileFormat.ValueType:
                  The format of the file, either in URDF format or Viam's kinematic parameter format (spatial vector algebra).

                - bytes: The byte contents of the file.
        """
        f = open("/home/nat/yahboom_template/src/dofbot.json", "rb")

        data = f.read()
        f.close()
        return (KinematicsFileFormat.KINEMATICS_FILE_FORMAT_SVA, data)

    async def read_servo(self, id):
        if id < 1 or id > 6:
            print("id must be 1 - 5")
            return None
        try:
            self.bus.write_byte_data(self.addr, id + 0x30, 0x0)
            time.sleep(0.003)
            pos = self.bus.read_word_data(self.addr, id + 0x30)
        except Exception as e:
            LOGGER.info(f'error at id {id}, err {e}')
            print('Arm_serial_servo_read I2C error')
            return None
        if pos == 0:
            return None
        pos = (pos >> 8 & 0xff) | (pos << 8 & 0xff00)
        if id == 5:
            pos = int((270 - 0) * (pos - 380) / (3700 - 380) + 0)
            if pos > 270 or pos < 0:
                return None
        else:
            pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
            if pos > 180 or pos < 0:
                return None
        if id == 2 or id == 3 or id == 4:
            pos = 180 - pos
        return pos
    
    async def write_all_servos(self, positions, time):
        s1, s2, s3, s4, s5 = positions.values
        s6 = 90

        if s1 > 180 or s2 > 180 or s3 > 180 or s4 > 180 or s5 > 270 or s6 > 180:
            LOGGER.error(f'attempted to write invalid angles to servos')
            return
        try:
            pos = int((3100 - 900) * (s1 - 0) / (180 - 0) + 900)
            value1_H = (pos >> 8) & 0xFF
            value1_L = pos & 0xFF

            s2 = 180 - s2
            pos = int((3100 - 900) * (s2 - 0) / (180 - 0) + 900)
            value2_H = (pos >> 8) & 0xFF
            value2_L = pos & 0xFF

            s3 = 180 - s3
            pos = int((3100 - 900) * (s3 - 0) / (180 - 0) + 900)
            value3_H = (pos >> 8) & 0xFF
            value3_L = pos & 0xFF

            s4 = 180 - s4
            pos = int((3100 - 900) * (s4 - 0) / (180 - 0) + 900)
            value4_H = (pos >> 8) & 0xFF
            value4_L = pos & 0xFF

            pos = int((3700 - 380) * (s5 - 0) / (270 - 0) + 380)
            value5_H = (pos >> 8) & 0xFF
            value5_L = pos & 0xFF

            pos = int((3100 - 900) * (s6 - 0) / (180 - 0) + 900)
            value6_H = (pos >> 8) & 0xFF
            value6_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF

            data = [value1_H, value1_L, value2_H, value2_L, value3_H, value3_L,
                    value4_H, value4_L, value5_H, value5_L, value6_H, value6_L]
            timeArr = [time_H, time_L]
            s_id = 0x1d
            self.bus.write_i2c_block_data(self.addr, 0x1e, timeArr)
            self.bus.write_i2c_block_data(self.addr, s_id, data)
        except Exception as e:
            LOGGER.info(f'write_all_servos error: {e}')
            return