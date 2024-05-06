#! /usr/bin/env python3


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn, Kill, SetPen
from time import sleep

class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher = self.create_publisher(
            msg_type=Twist,
            topic="/turtle1/cmd_vel",
            qos_profile=10
        )

    def desenhar(self):
        msg = Twist()
        msg.linear.x = 1.0
        msg.angular.z = 1.0
        self.publisher.publish(msg)
        #self.get_logger().info("Publicando velocidades para a tortuguita")


    def spawnar_tartaruga(self, x, y, theta):
        spawn_client = self.create_client(Spawn, 'spawn')
        while not spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('spawnar_tartaruga não disponível')
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = 'turtle1'
        future = spawn_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def kill_turtle(self):
        kill_client = self.create_client(Kill, 'kill')
        while not kill_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('kill_turtle não disponível')
        request = Kill.Request()
        request.name = 'turtle1'
        future = kill_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def set_pen(self, r, g, b):
        set_pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        while not set_pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('set_pen não disponível')
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = 5
        request.off = False
        future = set_pen_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

def main(args=None):
    rclpy.init(args=args)
    tc = TurtleController()
    tc.kill_turtle()
    sleep(1)
    tc.spawnar_tartaruga(5.0, 5.0, 0.0)
    tc.set_pen(255, 0, 255)
    for i in range(0, 8):
        tc.desenhar()
        sleep(1)
    tc.kill_turtle()
    tc.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

