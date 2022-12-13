;; Auto-generated. Do not edit!


(when (boundp 'bench::BenchMotorControl)
  (if (not (find-package "BENCH"))
    (make-package "BENCH"))
  (shadow 'BenchMotorControl (find-package "BENCH")))
(unless (find-package "BENCH::BENCHMOTORCONTROL")
  (make-package "BENCH::BENCHMOTORCONTROL"))

(in-package "ROS")
;;//! \htmlinclude BenchMotorControl.msg.html


(defclass bench::BenchMotorControl
  :super ros::object
  :slots (_flex_myobrick_pwm _extend_myobrick_pwm _flex_myobrick_start _extend_myobrick_start _reset_kill_switch _press_kill_switch ))

(defmethod bench::BenchMotorControl
  (:init
   (&key
    ((:flex_myobrick_pwm __flex_myobrick_pwm) 0.0)
    ((:extend_myobrick_pwm __extend_myobrick_pwm) 0.0)
    ((:flex_myobrick_start __flex_myobrick_start) nil)
    ((:extend_myobrick_start __extend_myobrick_start) nil)
    ((:reset_kill_switch __reset_kill_switch) nil)
    ((:press_kill_switch __press_kill_switch) nil)
    )
   (send-super :init)
   (setq _flex_myobrick_pwm (float __flex_myobrick_pwm))
   (setq _extend_myobrick_pwm (float __extend_myobrick_pwm))
   (setq _flex_myobrick_start __flex_myobrick_start)
   (setq _extend_myobrick_start __extend_myobrick_start)
   (setq _reset_kill_switch __reset_kill_switch)
   (setq _press_kill_switch __press_kill_switch)
   self)
  (:flex_myobrick_pwm
   (&optional __flex_myobrick_pwm)
   (if __flex_myobrick_pwm (setq _flex_myobrick_pwm __flex_myobrick_pwm)) _flex_myobrick_pwm)
  (:extend_myobrick_pwm
   (&optional __extend_myobrick_pwm)
   (if __extend_myobrick_pwm (setq _extend_myobrick_pwm __extend_myobrick_pwm)) _extend_myobrick_pwm)
  (:flex_myobrick_start
   (&optional (__flex_myobrick_start :null))
   (if (not (eq __flex_myobrick_start :null)) (setq _flex_myobrick_start __flex_myobrick_start)) _flex_myobrick_start)
  (:extend_myobrick_start
   (&optional (__extend_myobrick_start :null))
   (if (not (eq __extend_myobrick_start :null)) (setq _extend_myobrick_start __extend_myobrick_start)) _extend_myobrick_start)
  (:reset_kill_switch
   (&optional (__reset_kill_switch :null))
   (if (not (eq __reset_kill_switch :null)) (setq _reset_kill_switch __reset_kill_switch)) _reset_kill_switch)
  (:press_kill_switch
   (&optional (__press_kill_switch :null))
   (if (not (eq __press_kill_switch :null)) (setq _press_kill_switch __press_kill_switch)) _press_kill_switch)
  (:serialization-length
   ()
   (+
    ;; float32 _flex_myobrick_pwm
    4
    ;; float32 _extend_myobrick_pwm
    4
    ;; bool _flex_myobrick_start
    1
    ;; bool _extend_myobrick_start
    1
    ;; bool _reset_kill_switch
    1
    ;; bool _press_kill_switch
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _flex_myobrick_pwm
       (sys::poke _flex_myobrick_pwm (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _extend_myobrick_pwm
       (sys::poke _extend_myobrick_pwm (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _flex_myobrick_start
       (if _flex_myobrick_start (write-byte -1 s) (write-byte 0 s))
     ;; bool _extend_myobrick_start
       (if _extend_myobrick_start (write-byte -1 s) (write-byte 0 s))
     ;; bool _reset_kill_switch
       (if _reset_kill_switch (write-byte -1 s) (write-byte 0 s))
     ;; bool _press_kill_switch
       (if _press_kill_switch (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _flex_myobrick_pwm
     (setq _flex_myobrick_pwm (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _extend_myobrick_pwm
     (setq _extend_myobrick_pwm (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _flex_myobrick_start
     (setq _flex_myobrick_start (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _extend_myobrick_start
     (setq _extend_myobrick_start (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _reset_kill_switch
     (setq _reset_kill_switch (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _press_kill_switch
     (setq _press_kill_switch (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get bench::BenchMotorControl :md5sum-) "8ad18a25d3f99a657d5431e717084b05")
(setf (get bench::BenchMotorControl :datatype-) "bench/BenchMotorControl")
(setf (get bench::BenchMotorControl :definition-)
      "float32 flex_myobrick_pwm
float32 extend_myobrick_pwm

bool flex_myobrick_start
bool extend_myobrick_start

bool reset_kill_switch
bool press_kill_switch
")



(provide :bench/BenchMotorControl "8ad18a25d3f99a657d5431e717084b05")


