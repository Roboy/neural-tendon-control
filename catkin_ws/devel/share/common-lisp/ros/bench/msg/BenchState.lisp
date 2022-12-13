; Auto-generated. Do not edit!


(cl:in-package bench-msg)


;//! \htmlinclude BenchState.msg.html

(cl:defclass <BenchState> (roslisp-msg-protocol:ros-message)
  ((angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0)
   (safety_switch_pressed
    :reader safety_switch_pressed
    :initarg :safety_switch_pressed
    :type cl:boolean
    :initform cl:nil)
   (flex_myobrick_pos_encoder
    :reader flex_myobrick_pos_encoder
    :initarg :flex_myobrick_pos_encoder
    :type cl:float
    :initform 0.0)
   (flex_myobrick_torque_encoder
    :reader flex_myobrick_torque_encoder
    :initarg :flex_myobrick_torque_encoder
    :type cl:float
    :initform 0.0)
   (flex_myobrick_current
    :reader flex_myobrick_current
    :initarg :flex_myobrick_current
    :type cl:float
    :initform 0.0)
   (flex_myobrick_pwm
    :reader flex_myobrick_pwm
    :initarg :flex_myobrick_pwm
    :type cl:float
    :initform 0.0)
   (flex_myobrick_in_running_state
    :reader flex_myobrick_in_running_state
    :initarg :flex_myobrick_in_running_state
    :type cl:boolean
    :initform cl:nil)
   (extend_myobrick_pos_encoder
    :reader extend_myobrick_pos_encoder
    :initarg :extend_myobrick_pos_encoder
    :type cl:float
    :initform 0.0)
   (extend_myobrick_torque_encoder
    :reader extend_myobrick_torque_encoder
    :initarg :extend_myobrick_torque_encoder
    :type cl:float
    :initform 0.0)
   (extend_myobrick_current
    :reader extend_myobrick_current
    :initarg :extend_myobrick_current
    :type cl:float
    :initform 0.0)
   (extend_myobrick_pwm
    :reader extend_myobrick_pwm
    :initarg :extend_myobrick_pwm
    :type cl:float
    :initform 0.0)
   (extend_myobrick_in_running_state
    :reader extend_myobrick_in_running_state
    :initarg :extend_myobrick_in_running_state
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass BenchState (<BenchState>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BenchState>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BenchState)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name bench-msg:<BenchState> is deprecated: use bench-msg:BenchState instead.")))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:angle-val is deprecated.  Use bench-msg:angle instead.")
  (angle m))

(cl:ensure-generic-function 'safety_switch_pressed-val :lambda-list '(m))
(cl:defmethod safety_switch_pressed-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:safety_switch_pressed-val is deprecated.  Use bench-msg:safety_switch_pressed instead.")
  (safety_switch_pressed m))

(cl:ensure-generic-function 'flex_myobrick_pos_encoder-val :lambda-list '(m))
(cl:defmethod flex_myobrick_pos_encoder-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:flex_myobrick_pos_encoder-val is deprecated.  Use bench-msg:flex_myobrick_pos_encoder instead.")
  (flex_myobrick_pos_encoder m))

(cl:ensure-generic-function 'flex_myobrick_torque_encoder-val :lambda-list '(m))
(cl:defmethod flex_myobrick_torque_encoder-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:flex_myobrick_torque_encoder-val is deprecated.  Use bench-msg:flex_myobrick_torque_encoder instead.")
  (flex_myobrick_torque_encoder m))

(cl:ensure-generic-function 'flex_myobrick_current-val :lambda-list '(m))
(cl:defmethod flex_myobrick_current-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:flex_myobrick_current-val is deprecated.  Use bench-msg:flex_myobrick_current instead.")
  (flex_myobrick_current m))

(cl:ensure-generic-function 'flex_myobrick_pwm-val :lambda-list '(m))
(cl:defmethod flex_myobrick_pwm-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:flex_myobrick_pwm-val is deprecated.  Use bench-msg:flex_myobrick_pwm instead.")
  (flex_myobrick_pwm m))

(cl:ensure-generic-function 'flex_myobrick_in_running_state-val :lambda-list '(m))
(cl:defmethod flex_myobrick_in_running_state-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:flex_myobrick_in_running_state-val is deprecated.  Use bench-msg:flex_myobrick_in_running_state instead.")
  (flex_myobrick_in_running_state m))

(cl:ensure-generic-function 'extend_myobrick_pos_encoder-val :lambda-list '(m))
(cl:defmethod extend_myobrick_pos_encoder-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:extend_myobrick_pos_encoder-val is deprecated.  Use bench-msg:extend_myobrick_pos_encoder instead.")
  (extend_myobrick_pos_encoder m))

(cl:ensure-generic-function 'extend_myobrick_torque_encoder-val :lambda-list '(m))
(cl:defmethod extend_myobrick_torque_encoder-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:extend_myobrick_torque_encoder-val is deprecated.  Use bench-msg:extend_myobrick_torque_encoder instead.")
  (extend_myobrick_torque_encoder m))

(cl:ensure-generic-function 'extend_myobrick_current-val :lambda-list '(m))
(cl:defmethod extend_myobrick_current-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:extend_myobrick_current-val is deprecated.  Use bench-msg:extend_myobrick_current instead.")
  (extend_myobrick_current m))

(cl:ensure-generic-function 'extend_myobrick_pwm-val :lambda-list '(m))
(cl:defmethod extend_myobrick_pwm-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:extend_myobrick_pwm-val is deprecated.  Use bench-msg:extend_myobrick_pwm instead.")
  (extend_myobrick_pwm m))

(cl:ensure-generic-function 'extend_myobrick_in_running_state-val :lambda-list '(m))
(cl:defmethod extend_myobrick_in_running_state-val ((m <BenchState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:extend_myobrick_in_running_state-val is deprecated.  Use bench-msg:extend_myobrick_in_running_state instead.")
  (extend_myobrick_in_running_state m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BenchState>) ostream)
  "Serializes a message object of type '<BenchState>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'safety_switch_pressed) 1 0)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'flex_myobrick_pos_encoder))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'flex_myobrick_torque_encoder))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'flex_myobrick_current))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'flex_myobrick_pwm))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'flex_myobrick_in_running_state) 1 0)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'extend_myobrick_pos_encoder))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'extend_myobrick_torque_encoder))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'extend_myobrick_current))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'extend_myobrick_pwm))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'extend_myobrick_in_running_state) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BenchState>) istream)
  "Deserializes a message object of type '<BenchState>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'safety_switch_pressed) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'flex_myobrick_pos_encoder) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'flex_myobrick_torque_encoder) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'flex_myobrick_current) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'flex_myobrick_pwm) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'flex_myobrick_in_running_state) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'extend_myobrick_pos_encoder) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'extend_myobrick_torque_encoder) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'extend_myobrick_current) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'extend_myobrick_pwm) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'extend_myobrick_in_running_state) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BenchState>)))
  "Returns string type for a message object of type '<BenchState>"
  "bench/BenchState")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BenchState)))
  "Returns string type for a message object of type 'BenchState"
  "bench/BenchState")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BenchState>)))
  "Returns md5sum for a message object of type '<BenchState>"
  "5e6318cc4849f33a839d0d132a6048f8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BenchState)))
  "Returns md5sum for a message object of type 'BenchState"
  "5e6318cc4849f33a839d0d132a6048f8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BenchState>)))
  "Returns full string definition for message of type '<BenchState>"
  (cl:format cl:nil "float32 angle~%~%bool safety_switch_pressed~%~%float32 flex_myobrick_pos_encoder~%float32 flex_myobrick_torque_encoder~%float32 flex_myobrick_current~%float32 flex_myobrick_pwm~%bool flex_myobrick_in_running_state~%~%float32 extend_myobrick_pos_encoder~%float32 extend_myobrick_torque_encoder~%float32 extend_myobrick_current~%float32 extend_myobrick_pwm~%bool extend_myobrick_in_running_state~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BenchState)))
  "Returns full string definition for message of type 'BenchState"
  (cl:format cl:nil "float32 angle~%~%bool safety_switch_pressed~%~%float32 flex_myobrick_pos_encoder~%float32 flex_myobrick_torque_encoder~%float32 flex_myobrick_current~%float32 flex_myobrick_pwm~%bool flex_myobrick_in_running_state~%~%float32 extend_myobrick_pos_encoder~%float32 extend_myobrick_torque_encoder~%float32 extend_myobrick_current~%float32 extend_myobrick_pwm~%bool extend_myobrick_in_running_state~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BenchState>))
  (cl:+ 0
     4
     1
     4
     4
     4
     4
     1
     4
     4
     4
     4
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BenchState>))
  "Converts a ROS message object to a list"
  (cl:list 'BenchState
    (cl:cons ':angle (angle msg))
    (cl:cons ':safety_switch_pressed (safety_switch_pressed msg))
    (cl:cons ':flex_myobrick_pos_encoder (flex_myobrick_pos_encoder msg))
    (cl:cons ':flex_myobrick_torque_encoder (flex_myobrick_torque_encoder msg))
    (cl:cons ':flex_myobrick_current (flex_myobrick_current msg))
    (cl:cons ':flex_myobrick_pwm (flex_myobrick_pwm msg))
    (cl:cons ':flex_myobrick_in_running_state (flex_myobrick_in_running_state msg))
    (cl:cons ':extend_myobrick_pos_encoder (extend_myobrick_pos_encoder msg))
    (cl:cons ':extend_myobrick_torque_encoder (extend_myobrick_torque_encoder msg))
    (cl:cons ':extend_myobrick_current (extend_myobrick_current msg))
    (cl:cons ':extend_myobrick_pwm (extend_myobrick_pwm msg))
    (cl:cons ':extend_myobrick_in_running_state (extend_myobrick_in_running_state msg))
))
