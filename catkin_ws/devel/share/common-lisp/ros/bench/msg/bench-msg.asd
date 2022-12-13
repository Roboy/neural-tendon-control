
(cl:in-package :asdf)

(defsystem "bench-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "BenchMotorControl" :depends-on ("_package_BenchMotorControl"))
    (:file "_package_BenchMotorControl" :depends-on ("_package"))
    (:file "BenchRecorderControl" :depends-on ("_package_BenchRecorderControl"))
    (:file "_package_BenchRecorderControl" :depends-on ("_package"))
    (:file "BenchState" :depends-on ("_package_BenchState"))
    (:file "_package_BenchState" :depends-on ("_package"))
  ))