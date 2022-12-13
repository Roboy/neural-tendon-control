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

class BenchMotorControl {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.flex_myobrick_pwm = null;
      this.extend_myobrick_pwm = null;
      this.flex_myobrick_start = null;
      this.extend_myobrick_start = null;
      this.reset_kill_switch = null;
      this.press_kill_switch = null;
    }
    else {
      if (initObj.hasOwnProperty('flex_myobrick_pwm')) {
        this.flex_myobrick_pwm = initObj.flex_myobrick_pwm
      }
      else {
        this.flex_myobrick_pwm = 0.0;
      }
      if (initObj.hasOwnProperty('extend_myobrick_pwm')) {
        this.extend_myobrick_pwm = initObj.extend_myobrick_pwm
      }
      else {
        this.extend_myobrick_pwm = 0.0;
      }
      if (initObj.hasOwnProperty('flex_myobrick_start')) {
        this.flex_myobrick_start = initObj.flex_myobrick_start
      }
      else {
        this.flex_myobrick_start = false;
      }
      if (initObj.hasOwnProperty('extend_myobrick_start')) {
        this.extend_myobrick_start = initObj.extend_myobrick_start
      }
      else {
        this.extend_myobrick_start = false;
      }
      if (initObj.hasOwnProperty('reset_kill_switch')) {
        this.reset_kill_switch = initObj.reset_kill_switch
      }
      else {
        this.reset_kill_switch = false;
      }
      if (initObj.hasOwnProperty('press_kill_switch')) {
        this.press_kill_switch = initObj.press_kill_switch
      }
      else {
        this.press_kill_switch = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type BenchMotorControl
    // Serialize message field [flex_myobrick_pwm]
    bufferOffset = _serializer.float32(obj.flex_myobrick_pwm, buffer, bufferOffset);
    // Serialize message field [extend_myobrick_pwm]
    bufferOffset = _serializer.float32(obj.extend_myobrick_pwm, buffer, bufferOffset);
    // Serialize message field [flex_myobrick_start]
    bufferOffset = _serializer.bool(obj.flex_myobrick_start, buffer, bufferOffset);
    // Serialize message field [extend_myobrick_start]
    bufferOffset = _serializer.bool(obj.extend_myobrick_start, buffer, bufferOffset);
    // Serialize message field [reset_kill_switch]
    bufferOffset = _serializer.bool(obj.reset_kill_switch, buffer, bufferOffset);
    // Serialize message field [press_kill_switch]
    bufferOffset = _serializer.bool(obj.press_kill_switch, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type BenchMotorControl
    let len;
    let data = new BenchMotorControl(null);
    // Deserialize message field [flex_myobrick_pwm]
    data.flex_myobrick_pwm = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [extend_myobrick_pwm]
    data.extend_myobrick_pwm = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [flex_myobrick_start]
    data.flex_myobrick_start = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [extend_myobrick_start]
    data.extend_myobrick_start = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [reset_kill_switch]
    data.reset_kill_switch = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [press_kill_switch]
    data.press_kill_switch = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'bench/BenchMotorControl';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '8ad18a25d3f99a657d5431e717084b05';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 flex_myobrick_pwm
    float32 extend_myobrick_pwm
    
    bool flex_myobrick_start
    bool extend_myobrick_start
    
    bool reset_kill_switch
    bool press_kill_switch
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new BenchMotorControl(null);
    if (msg.flex_myobrick_pwm !== undefined) {
      resolved.flex_myobrick_pwm = msg.flex_myobrick_pwm;
    }
    else {
      resolved.flex_myobrick_pwm = 0.0
    }

    if (msg.extend_myobrick_pwm !== undefined) {
      resolved.extend_myobrick_pwm = msg.extend_myobrick_pwm;
    }
    else {
      resolved.extend_myobrick_pwm = 0.0
    }

    if (msg.flex_myobrick_start !== undefined) {
      resolved.flex_myobrick_start = msg.flex_myobrick_start;
    }
    else {
      resolved.flex_myobrick_start = false
    }

    if (msg.extend_myobrick_start !== undefined) {
      resolved.extend_myobrick_start = msg.extend_myobrick_start;
    }
    else {
      resolved.extend_myobrick_start = false
    }

    if (msg.reset_kill_switch !== undefined) {
      resolved.reset_kill_switch = msg.reset_kill_switch;
    }
    else {
      resolved.reset_kill_switch = false
    }

    if (msg.press_kill_switch !== undefined) {
      resolved.press_kill_switch = msg.press_kill_switch;
    }
    else {
      resolved.press_kill_switch = false
    }

    return resolved;
    }
};

module.exports = BenchMotorControl;
