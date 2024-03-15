# The yahboom arm

This module interfaces with a Yahboom [Dofbot](https://category.yahboom.net/products/dofbot-jetson_nano) robotic arm. It implements the machine as a modular Viam Arm and a modular Viam Gripper.


## Capabilities
The arm currently implements `get_joint_positions`, `move_to_joint_positions`, `stop` and `get_kinematics`. Other Viam Arm APIs will be added.
The gripper implements all Viam Gripper APIs.


## Configuration

The arm requires no attirbutes to configure. Add an arm component from your module. The gripper requires the name of the arm it is attached to as an attirbute.

### `rand:yahboom:dofbot`
```json
{
  "modules": [
    {
      "name": "yahboom",
      "executable_path": "path/to/run.sh"
    }
  ],
  "components": [
    {
      "model": "rand:yahboom:arm",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": [],
      "type": "arm",
      "name": "armie"
    },
    {
      "model": "rand:yahboom:gripper",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": [],
      "type": "gripper",
      "name": "grippie"
    }
  ]
}
```
