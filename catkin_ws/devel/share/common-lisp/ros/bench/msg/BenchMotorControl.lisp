; Auto-generated. Do not edit!


(cl:in-package bench-msg)


;//! \htmlinclude BenchMotorControl.msg.html

(cl:defclass <BenchMotorControl> (roslisp-msg-protocol:ros-message)
  ((flex_myobrick_pwm
    :reader flex_myobrick_pwm
    :initarg :flex_myobrick_pwm
    :type cl:float
    :initform 0.0)
   (extend_myobrick_pwm
    :reader extend_myobrick_pwm
    :initarg :extend_myobrick_pwm
    :type cl:float
    :initform 0.0)
   (flex_myobrick_start
    :reader flex_myobrick_start
    :initarg :flex_myobrick_start
    :type cl:boolean
    :initform cl:nil)
   (extend_myobrick_start
    :reader extend_myobrick_start
    :initarg :extend_myobrick_start
    :type cl:boolean
    :initform cl:nil)
   (reset_kill_switch
    :reader reset_kill_switch
    :initarg :reset_kill_switch
    :type cl:boolean
    :initform cl:nil)
   (press_kill_switch
    :reader press_kill_switch
    :initarg :press_kill_switch
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass BenchMotorControl (<BenchMotorControl>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BenchMotorControl>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BenchMotorControl)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name bench-msg:<BenchMotorControl> is deprecated: use bench-msg:BenchMotorControl instead.")))

(cl:ensure-generic-function 'flex_myobrick_pwm-val :lambda-list '(m))
(cl:defmethod flex_myobrick_pwm-val ((m <BenchMotorControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:flex_myobrick_pwm-val is deprecated.  Use bench-msg:flex_myobrick_pwm instead.")
  (flex_myobrick_pwm m))

(cl:ensure-generic-function 'extend_myobrick_pwm-val :lambda-list '(m))
(cl:defmethod extend_myobrick_pwm-val ((m <BenchMotorControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:extend_myobrick_pwm-val is deprecated.  Use bench-msg:extend_myobrick_pwm instead.")
  (extend_myobrick_pwm m))

(cl:ensure-generic-function 'flex_myobrick_start-val :lambda-list '(m))
(cl:defmethod flex_myobrick_start-val ((m <BenchMotorControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:flex_myobrick_start-val is deprecated.  Use bench-msg:flex_myobrick_start instead.")
  (flex_myobrick_start m))

(cl:ensure-generic-function 'extend_myobrick_start-val :lambda-list '(m))
(cl:defmethod extend_myobrick_start-val ((m <BenchMotorControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:extend_myobrick_start-val is deprecated.  Use bench-msg:extend_myobrick_start instead.")
  (extend_myobrick_start m))

(cl:ensure-generic-function 'reset_kill_switch-val :lambda-list '(m))
(cl:defmethod reset_kill_switch-val ((m <BenchMotorControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:reset_kill_switch-val is deprecated.  Use bench-msg:reset_kill_switch instead.")
  (reset_kill_switch m))

(cl:ensure-generic-function 'press_kill_switch-val :lambda-list '(m))
(cl:defmethod press_kill_switch-val ((m <BenchMotorControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:press_kill_switch-val is deprecated.  Use bench-msg:press_kill_switch instead.")
  (press_kill_switch m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BenchMotorControl>) ostream)
  "Serializes a message object of type '<BenchMotorControl>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'flex_myobrick_pwm))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'extend_myobrick_pwm))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'flex_myobrick_start) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'extend_myobrick_start) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'reset_kill_switch) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'press_kill_switch) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BenchMotorControl>) istream)
  "Deserializes a message object of type '<BenchMotorControl>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'flex_myobrick_pwm) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'extend_myobrick_pwm) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'flex_myobrick_start) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'extend_myobrick_start) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'reset_kill_switch) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'press_kill_switch) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BenchMotorControl>)))
  "Returns string type for a message object of type '<BenchMotorControl>"
  "bench/BenchMotorControl")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BenchMotorControl)))
  "Returns string type for a message object of type 'BenchMotorControl"
  "bench/BenchMotorControl")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BenchMotorControl>)))
  "Returns md5sum for a message object of type '<BenchMotorControl>"
  "8ad18a25d3f99a657d5431e717084b05")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BenchMotorControl)))
  "Returns md5sum for a message object of type 'BenchMotorControl"
  "8ad18a25d3f99a657d5431e717084b05")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BenchMotorControl>)))
  "Returns full string definition for message of type '<BenchMotorControl>"
  (cl:format cl:nil "float32 flex_myobrick_pwm~%float32 extend_myobrick_pwm~%~%bool flex_myobrick_start~%bool extend_myobrick_start~%~%bool reset_kill_switch~%bool press_kill_switch~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BenchMotorControl)))
  "Returns full string definition for message of type 'BenchMotorControl"
  (cl:format cl:nil "float32 flex_myobrick_pwm~%float32 extend_myobrick_pwm~%~%bool flex_myobrick_start~%bool extend_myobrick_start~%~%bool reset_kill_switch~%bool press_kill_switch~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BenchMotorControl>))
  (cl:+ 0
     4
     4
     1
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BenchMotorControl>))
  "Converts a ROS message object to a list"
  (cl:list 'BenchMotorControl
    (cl:cons ':flex_myobrick_pwm (flex_myobrick_pwm msg))
    (cl:cons ':extend_myobrick_pwm (extend_myobrick_pwm msg))
    (cl:cons ':flex_myobrick_start (flex_myobrick_start msg))
    (cl:cons ':extend_myobrick_start (extend_myobrick_start msg))
    (cl:cons ':reset_kill_switch (reset_kill_switch msg))
    (cl:cons ':press_kill_switch (press_kill_switch msg))
))
