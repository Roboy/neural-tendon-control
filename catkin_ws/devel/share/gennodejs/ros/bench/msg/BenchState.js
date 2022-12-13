// Auto-generated. Do not edit!

// (in-package bench.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class BenchState {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.angle = null;
      this.safety_switch_pressed = null;
      this.flex_myobrick_pos_encoder = null;
      this.flex_myobrick_torque_encoder = null;
      this.flex_myobrick_current = null;
      this.flex_myobrick_pwm = null;
      this.flex_myobrick_in_running_state = null;
      this.extend_myobrick_pos_encoder = null;
      this.extend_myobrick_torque_encoder = null;
      this.extend_myobrick_current = null;
      this.extend_myobrick_pwm = null;
      this.extend_myobrick_in_running_state = null;
    }
    else {
      if (initObj.hasOwnProperty('angle')) {
        this.angle = initObj.angle
      }
      else {
        this.angle = 0.0;
      }
      if (initObj.hasOwnProperty('safety_switch_pressed')) {
        this.safety_switch_pressed = initObj.safety_switch_pressed
      }
      else {
        this.safety_switch_pressed = false;
      }
      if (initObj.hasOwnProperty('flex_myobrick_pos_encoder')) {
        this.flex_myobrick_pos_encoder = initObj.flex_myobrick_pos_encoder
      }
      else {
        this.flex_myobrick_pos_encoder = 0.0;
      }
      if (initObj.hasOwnProperty('flex_myobrick_torque_encoder')) {
        this.flex_myobrick_torque_encoder = initObj.flex_myobrick_torque_encoder
      }
      else {
        this.flex_myobrick_torque_encoder = 0.0;
      }
      if (initObj.hasOwnProperty('flex_myobrick_current')) {
        this.flex_myobrick_current = initObj.flex_myobrick_current
      }
      else {
        this.flex_myobrick_current = 0.0;
      }
      if (initObj.hasOwnProperty('flex_myobrick_pwm')) {
        this.flex_myobrick_pwm = initObj.flex_myobrick_pwm
      }
      else {
        this.flex_myobrick_pwm = 0.0;
      }
      if (initObj.hasOwnProperty('flex_myobrick_in_running_state')) {
        this.flex_myobrick_in_running_state = initObj.flex_myobrick_in_running_state
      }
      else {
        this.flex_myobrick_in_running_state = false;
      }
      if (initObj.hasOwnProperty('extend_myobrick_pos_encoder')) {
        this.extend_myobrick_pos_encoder = initObj.extend_myobrick_pos_encoder
      }
      else {
        this.extend_myobrick_pos_encoder = 0.0;
      }
      if (initObj.hasOwnProperty('extend_myobrick_torque_encoder')) {
        this.extend_myobrick_torque_encoder = initObj.extend_myobrick_torque_encoder
      }
      else {
        this.extend_myobrick_torque_encoder = 0.0;
      }
      if (initObj.hasOwnProperty('extend_myobrick_current')) {
        this.extend_myobrick_current = initObj.extend_myobrick_current
      }
      else {
        this.extend_myobrick_current = 0.0;
      }
      if (initObj.hasOwnProperty('extend_myobrick_pwm')) {
        this.extend_myobrick_pwm = initObj.extend_myobrick_pwm
      }
      else {
        this.extend_myobrick_pwm = 0.0;
      }
      if (initObj.hasOwnProperty('extend_myobrick_in_running_state')) {
        this.extend_myobrick_in_running_state = initObj.extend_myobrick_in_running_state
      }
      else {
        this.extend_myobrick_in_running_state = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type BenchState
    // Serialize message field [angle]
    bufferOffset = _serializer.float32(obj.angle, buffer, bufferOffset);
    // Serialize message field [safety_switch_pressed]
    bufferOffset = _serializer.bool(obj.safety_switch_pressed, buffer, bufferOffset);
    // Serialize message field [flex_myobrick_pos_encoder]
    bufferOffset = _serializer.float32(obj.flex_myobrick_pos_encoder, buffer, bufferOffset);
    // Serialize message field [flex_myobrick_torque_encoder]
    bufferOffset = _serializer.float32(obj.flex_myobrick_torque_encoder, buffer, bufferOffset);
    // Serialize message field [flex_myobrick_current]
    bufferOffset = _serializer.float32(obj.flex_myobrick_current, buffer, bufferOffset);
    // Serialize message field [flex_myobrick_pwm]
    bufferOffset = _serializer.float32(obj.flex_myobrick_pwm, buffer, bufferOffset);
    // Serialize message field [flex_myobrick_in_running_state]
    bufferOffset = _serializer.bool(obj.flex_myobrick_in_running_state, buffer, bufferOffset);
    // Serialize message field [extend_myobrick_pos_encoder]
    bufferOffset = _serializer.float32(obj.extend_myobrick_pos_encoder, buffer, bufferOffset);
    // Serialize message field [extend_myobrick_torque_encoder]
    bufferOffset = _serializer.float32(obj.extend_myobrick_torque_encoder, buffer, bufferOffset);
    // Serialize message field [extend_myobrick_current]
    bufferOffset = _serializer.float32(obj.extend_myobrick_current, buffer, bufferOffset);
    // Serialize message field [extend_myobrick_pwm]
    bufferOffset = _serializer.float32(obj.extend_myobrick_pwm, buffer, bufferOffset);
    // Serialize message field [extend_myobrick_in_running_state]
    bufferOffset = _serializer.bool(obj.extend_myobrick_in_running_state, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type BenchState
    let len;
    let data = new BenchState(null);
    // Deserialize message field [angle]
    data.angle = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [safety_switch_pressed]
    data.safety_switch_pressed = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [flex_myobrick_pos_encoder]
    data.flex_myobrick_pos_encoder = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [flex_myobrick_torque_encoder]
    data.flex_myobrick_torque_encoder = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [flex_myobrick_current]
    data.flex_myobrick_current = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [flex_myobrick_pwm]
    data.flex_myobrick_pwm = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [flex_myobrick_in_running_state]
    data.flex_myobrick_in_running_state = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [extend_myobrick_pos_encoder]
    data.extend_myobrick_pos_encoder = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [extend_myobrick_torque_encoder]
    data.extend_myobrick_torque_encoder = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [extend_myobrick_current]
    data.extend_myobrick_current = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [extend_myobrick_pwm]
    data.extend_myobrick_pwm = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [extend_myobrick_in_running_state]
    data.extend_myobrick_in_running_state = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 39;
  }

  static datatype() {
    // Returns string type for a message object
    return 'bench/BenchState';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '5e6318cc4849f33a839d0d132a6048f8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 angle
    
    bool safety_switch_pressed
    
    float32 flex_myobrick_pos_encoder
    float32 flex_myobrick_torque_encoder
    float32 flex_myobrick_current
    float32 flex_myobrick_pwm
    bool flex_myobrick_in_running_state
    
    float32 extend_myobrick_pos_encoder
    float32 extend_myobrick_torque_encoder
    float32 extend_myobrick_current
    float32 extend_myobrick_pwm
    bool extend_myobrick_in_running_state
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new BenchState(null);
    if (msg.angle !== undefined) {
      resolved.angle = msg.angle;
    }
    else {
      resolved.angle = 0.0
    }

    if (msg.safety_switch_pressed !== undefined) {
      resolved.safety_switch_pressed = msg.safety_switch_pressed;
    }
    else {
      resolved.safety_switch_pressed = false
    }

    if (msg.flex_myobrick_pos_encoder !== undefined) {
      resolved.flex_myobrick_pos_encoder = msg.flex_myobrick_pos_encoder;
    }
    else {
      resolved.flex_myobrick_pos_encoder = 0.0
    }

    if (msg.flex_myobrick_torque_encoder !== undefined) {
      resolved.flex_myobrick_torque_encoder = msg.flex_myobrick_torque_encoder;
    }
    else {
      resolved.flex_myobrick_torque_encoder = 0.0
    }

    if (msg.flex_myobrick_current !== undefined) {
      resolved.flex_myobrick_current = msg.flex_myobrick_current;
    }
    else {
      resolved.flex_myobrick_current = 0.0
    }

    if (msg.flex_myobrick_pwm !== undefined) {
      resolved.flex_myobrick_pwm = msg.flex_myobrick_pwm;
    }
    else {
      resolved.flex_myobrick_pwm = 0.0
    }

    if (msg.flex_myobrick_in_running_state !== undefined) {
      resolved.flex_myobrick_in_running_state = msg.flex_myobrick_in_running_state;
    }
    else {
      resolved.flex_myobrick_in_running_state = false
    }

    if (msg.extend_myobrick_pos_encoder !== undefined) {
      resolved.extend_myobrick_pos_encoder = msg.extend_myobrick_pos_encoder;
    }
    else {
      resolved.extend_myobrick_pos_encoder = 0.0
    }

    if (msg.extend_myobrick_torque_encoder !== undefined) {
      resolved.extend_myobrick_torque_encoder = msg.extend_myobrick_torque_encoder;
    }
    else {
      resolved.extend_myobrick_torque_encoder = 0.0
    }

    if (msg.extend_myobrick_current !== undefined) {
      resolved.extend_myobrick_current = msg.extend_myobrick_current;
    }
    else {
      resolved.extend_myobrick_current = 0.0
    }

    if (msg.extend_myobrick_pwm !== undefined) {
      resolved.extend_myobrick_pwm = msg.extend_myobrick_pwm;
    }
    else {
      resolved.extend_myobrick_pwm = 0.0
    }

    if (msg.extend_myobrick_in_running_state !== undefined) {
      resolved.extend_myobrick_in_running_state = msg.extend_myobrick_in_running_state;
    }
    else {
      resolved.extend_myobrick_in_running_state = false
    }

    return resolved;
    }
};

module.exports = BenchState;
