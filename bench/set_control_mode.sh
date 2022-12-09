echo "Configuring motor $1 to PWM mode."

rosservice call /roboy/pinky/middleware/ControlMode "control_mode: 3
set_points: [0]
global_id: [$1]"