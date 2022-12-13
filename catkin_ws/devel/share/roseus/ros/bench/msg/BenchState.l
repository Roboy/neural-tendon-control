;; Auto-generated. Do not edit!


(when (boundp 'bench::BenchState)
  (if (not (find-package "BENCH"))
    (make-package "BENCH"))
  (shadow 'BenchState (find-package "BENCH")))
(unless (find-package "BENCH::BENCHSTATE")
  (make-package "BENCH::BENCHSTATE"))

(in-package "ROS")
;;//! \htmlinclude BenchState.msg.html


(defclass bench::BenchState
  :super ros::object
  :slots (_angle _safety_switch_pressed _flex_myobrick_pos_encoder _flex_myobrick_torque_encoder _flex_myobrick_current _flex_myobrick_pwm _flex_myobrick_in_running_state _extend_myobrick_pos_encoder _extend_myobrick_torque_encoder _extend_myobrick_current _extend_myobrick_pwm _extend_myobrick_in_running_state ))

(defmethod bench::BenchState
  (:init
   (&key
    ((:angle __angle) 0.0)
    ((:safety_switch_pressed __safety_switch_pressed) nil)
    ((:flex_myobrick_pos_encoder __flex_myobrick_pos_encoder) 0.0)
    ((:flex_myobrick_torque_encoder __flex_myobrick_torque_encoder) 0.0)
    ((:flex_myobrick_current __flex_myobrick_current) 0.0)
    ((:flex_myobrick_pwm __flex_myobrick_pwm) 0.0)
    ((:flex_myobrick_in_running_state __flex_myobrick_in_running_state) nil)
    ((:extend_myobrick_pos_encoder __extend_myobrick_pos_encoder) 0.0)
    ((:extend_myobrick_torque_encoder __extend_myobrick_torque_encoder) 0.0)
    ((:extend_myobrick_current __extend_myobrick_current) 0.0)
    ((:extend_myobrick_pwm __extend_myobrick_pwm) 0.0)
    ((:extend_myobrick_in_running_state __extend_myobrick_in_running_state) nil)
    )
   (send-super :init)
   (setq _angle (float __angle))
   (setq _safety_switch_pressed __safety_switch_pressed)
   (setq _flex_myobrick_pos_encoder (float __flex_myobrick_pos_encoder))
   (setq _flex_myobrick_torque_encoder (float __flex_myobrick_torque_encoder))
   (setq _flex_myobrick_current (float __flex_myobrick_current))
   (setq _flex_myobrick_pwm (float __flex_myobrick_pwm))
   (setq _flex_myobrick_in_running_state __flex_myobrick_in_running_state)
   (setq _extend_myobrick_pos_encoder (float __extend_myobrick_pos_encoder))
   (setq _extend_myobrick_torque_encoder (float __extend_myobrick_torque_encoder))
   (setq _extend_myobrick_current (float __extend_myobrick_current))
   (setq _extend_myobrick_pwm (float __extend_myobrick_pwm))
   (setq _extend_myobrick_in_running_state __extend_myobrick_in_running_state)
   self)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:safety_switch_pressed
   (&optional (__safety_switch_pressed :null))
   (if (not (eq __safety_switch_pressed :null)) (setq _safety_switch_pressed __safety_switch_pressed)) _safety_switch_pressed)
  (:flex_myobrick_pos_encoder
   (&optional __flex_myobrick_pos_encoder)
   (if __flex_myobrick_pos_encoder (setq _flex_myobrick_pos_encoder __flex_myobrick_pos_encoder)) _flex_myobrick_pos_encoder)
  (:flex_myobrick_torque_encoder
   (&optional __flex_myobrick_torque_encoder)
   (if __flex_myobrick_torque_encoder (setq _flex_myobrick_torque_encoder __flex_myobrick_torque_encoder)) _flex_myobrick_torque_encoder)
  (:flex_myobrick_current
   (&optional __flex_myobrick_current)
   (if __flex_myobrick_current (setq _flex_myobrick_current __flex_myobrick_current)) _flex_myobrick_current)
  (:flex_myobrick_pwm
   (&optional __flex_myobrick_pwm)
   (if __flex_myobrick_pwm (setq _flex_myobrick_pwm __flex_myobrick_pwm)) _flex_myobrick_pwm)
  (:flex_myobrick_in_running_state
   (&optional (__flex_myobrick_in_running_state :null))
   (if (not (eq __flex_myobrick_in_running_state :null)) (setq _flex_myobrick_in_running_state __flex_myobrick_in_running_state)) _flex_myobrick_in_running_state)
  (:extend_myobrick_pos_encoder
   (&optional __extend_myobrick_pos_encoder)
   (if __extend_myobrick_pos_encoder (setq _extend_myobrick_pos_encoder __extend_myobrick_pos_encoder)) _extend_myobrick_pos_encoder)
  (:extend_myobrick_torque_encoder
   (&optional __extend_myobrick_torque_encoder)
   (if __extend_myobrick_torque_encoder (setq _extend_myobrick_torque_encoder __extend_myobrick_torque_encoder)) _extend_myobrick_torque_encoder)
  (:extend_myobrick_current
   (&optional __extend_myobrick_current)
   (if __extend_myobrick_current (setq _extend_myobrick_current __extend_myobrick_current)) _extend_myobrick_current)
  (:extend_myobrick_pwm
   (&optional __extend_myobrick_pwm)
   (if __extend_myobrick_pwm (setq _extend_myobrick_pwm __extend_myobrick_pwm)) _extend_myobrick_pwm)
  (:extend_myobrick_in_running_state
   (&optional (__extend_myobrick_in_running_state :null))
   (if (not (eq __extend_myobrick_in_running_state :null)) (setq _extend_myobrick_in_running_state __extend_myobrick_in_running_state)) _extend_myobrick_in_running_state)
  (:serialization-length
   ()
   (+
    ;; float32 _angle
    4
    ;; bool _safety_switch_pressed
    1
    ;; float32 _flex_myobrick_pos_encoder
    4
    ;; float32 _flex_myobrick_torque_encoder
    4
    ;; float32 _flex_myobrick_current
    4
    ;; float32 _flex_myobrick_pwm
    4
    ;; bool _flex_myobrick_in_running_state
    1
    ;; float32 _extend_myobrick_pos_encoder
    4
    ;; float32 _extend_myobrick_torque_encoder
    4
    ;; float32 _extend_myobrick_current
    4
    ;; float32 _extend_myobrick_pwm
    4
    ;; bool _extend_myobrick_in_running_state
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _safety_switch_pressed
       (if _safety_switch_pressed (write-byte -1 s) (write-byte 0 s))
     ;; float32 _flex_myobrick_pos_encoder
       (sys::poke _flex_myobrick_pos_encoder (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _flex_myobrick_torque_encoder
       (sys::poke _flex_myobrick_torque_encoder (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _flex_myobrick_current
       (sys::poke _flex_myobrick_current (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _flex_myobrick_pwm
       (sys::poke _flex_myobrick_pwm (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _flex_myobrick_in_running_state
       (if _flex_myobrick_in_running_state (write-byte -1 s) (write-byte 0 s))
     ;; float32 _extend_myobrick_pos_encoder
       (sys::poke _extend_myobrick_pos_encoder (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _extend_myobrick_torque_encoder
       (sys::poke _extend_myobrick_torque_encoder (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _extend_myobrick_current
       (sys::poke _extend_myobrick_current (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _extend_myobrick_pwm
       (sys::poke _extend_myobrick_pwm (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _extend_myobrick_in_running_state
       (if _extend_myobrick_in_running_state (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _angle
     (setq _angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _safety_switch_pressed
     (setq _safety_switch_pressed (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float32 _flex_myobrick_pos_encoder
     (setq _flex_myobrick_pos_encoder (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _flex_myobrick_torque_encoder
     (setq _flex_myobrick_torque_encoder (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _flex_myobrick_current
     (setq _flex_myobrick_current (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _flex_myobrick_pwm
     (setq _flex_myobrick_pwm (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _flex_myobrick_in_running_state
     (setq _flex_myobrick_in_running_state (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float32 _extend_myobrick_pos_encoder
     (setq _extend_myobrick_pos_encoder (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _extend_myobrick_torque_encoder
     (setq _extend_myobrick_torque_encoder (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _extend_myobrick_current
     (setq _extend_myobrick_current (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _extend_myobrick_pwm
     (setq _extend_myobrick_pwm (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _extend_myobrick_in_running_state
     (setq _extend_myobrick_in_running_state (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get bench::BenchState :md5sum-) "5e6318cc4849f33a839d0d132a6048f8")
(setf (get bench::BenchState :datatype-) "bench/BenchState")
(setf (get bench::BenchState :definition-)
      "float32 angle

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


")



(provide :bench/BenchState "5e6318cc4849f33a839d0d132a6048f8")


