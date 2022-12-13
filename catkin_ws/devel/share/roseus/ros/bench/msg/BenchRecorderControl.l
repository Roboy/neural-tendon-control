;; Auto-generated. Do not edit!


(when (boundp 'bench::BenchRecorderControl)
  (if (not (find-package "BENCH"))
    (make-package "BENCH"))
  (shadow 'BenchRecorderControl (find-package "BENCH")))
(unless (find-package "BENCH::BENCHRECORDERCONTROL")
  (make-package "BENCH::BENCHRECORDERCONTROL"))

(in-package "ROS")
;;//! \htmlinclude BenchRecorderControl.msg.html


(defclass bench::BenchRecorderControl
  :super ros::object
  :slots (_path _duration ))

(defmethod bench::BenchRecorderControl
  (:init
   (&key
    ((:path __path) "")
    ((:duration __duration) 0.0)
    )
   (send-super :init)
   (setq _path (string __path))
   (setq _duration (float __duration))
   self)
  (:path
   (&optional __path)
   (if __path (setq _path __path)) _path)
  (:duration
   (&optional __duration)
   (if __duration (setq _duration __duration)) _duration)
  (:serialization-length
   ()
   (+
    ;; string _path
    4 (length _path)
    ;; float32 _duration
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _path
       (write-long (length _path) s) (princ _path s)
     ;; float32 _duration
       (sys::poke _duration (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _path
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _path (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32 _duration
     (setq _duration (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get bench::BenchRecorderControl :md5sum-) "7834feee666c6bae9219665e28ae929e")
(setf (get bench::BenchRecorderControl :datatype-) "bench/BenchRecorderControl")
(setf (get bench::BenchRecorderControl :definition-)
      "string path
float32 duration
")



(provide :bench/BenchRecorderControl "7834feee666c6bae9219665e28ae929e")


