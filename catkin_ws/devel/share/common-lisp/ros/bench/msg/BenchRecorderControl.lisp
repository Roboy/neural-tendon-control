; Auto-generated. Do not edit!


(cl:in-package bench-msg)


;//! \htmlinclude BenchRecorderControl.msg.html

(cl:defclass <BenchRecorderControl> (roslisp-msg-protocol:ros-message)
  ((path
    :reader path
    :initarg :path
    :type cl:string
    :initform "")
   (duration
    :reader duration
    :initarg :duration
    :type cl:float
    :initform 0.0))
)

(cl:defclass BenchRecorderControl (<BenchRecorderControl>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BenchRecorderControl>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BenchRecorderControl)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name bench-msg:<BenchRecorderControl> is deprecated: use bench-msg:BenchRecorderControl instead.")))

(cl:ensure-generic-function 'path-val :lambda-list '(m))
(cl:defmethod path-val ((m <BenchRecorderControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:path-val is deprecated.  Use bench-msg:path instead.")
  (path m))

(cl:ensure-generic-function 'duration-val :lambda-list '(m))
(cl:defmethod duration-val ((m <BenchRecorderControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader bench-msg:duration-val is deprecated.  Use bench-msg:duration instead.")
  (duration m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BenchRecorderControl>) ostream)
  "Serializes a message object of type '<BenchRecorderControl>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'path))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'path))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'duration))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BenchRecorderControl>) istream)
  "Deserializes a message object of type '<BenchRecorderControl>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'path) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'path) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'duration) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BenchRecorderControl>)))
  "Returns string type for a message object of type '<BenchRecorderControl>"
  "bench/BenchRecorderControl")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BenchRecorderControl)))
  "Returns string type for a message object of type 'BenchRecorderControl"
  "bench/BenchRecorderControl")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BenchRecorderControl>)))
  "Returns md5sum for a message object of type '<BenchRecorderControl>"
  "7834feee666c6bae9219665e28ae929e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BenchRecorderControl)))
  "Returns md5sum for a message object of type 'BenchRecorderControl"
  "7834feee666c6bae9219665e28ae929e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BenchRecorderControl>)))
  "Returns full string definition for message of type '<BenchRecorderControl>"
  (cl:format cl:nil "string path~%float32 duration~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BenchRecorderControl)))
  "Returns full string definition for message of type 'BenchRecorderControl"
  (cl:format cl:nil "string path~%float32 duration~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BenchRecorderControl>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'path))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BenchRecorderControl>))
  "Converts a ROS message object to a list"
  (cl:list 'BenchRecorderControl
    (cl:cons ':path (path msg))
    (cl:cons ':duration (duration msg))
))
