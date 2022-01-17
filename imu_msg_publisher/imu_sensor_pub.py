from opencr_imu_sensor_interface.msg import OpencrIMUSensor
import rclpy
from rclpy.node import Node
# from time import sleep
import time
import serial
import signal

def openSerial(port="/dev/ttyACM0", speed = 115200):
    try:
        s = serial.Serial(port, speed) 
            
    except serial.SerialException as e:
        if e.errno == 13:
            raise e
        pass
    except OSError:
        pass
    return s

ser = openSerial()
class CustomMsgPublisher(Node):

    def __init__(self):
        super().__init__('imu_sensor_publisher')
        self.publisher_ = self.create_publisher(OpencrIMUSensor, 'imu_sensor_topic', 10)
        # timer_period = 1
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0
        self.line = [] #라인 단위로 데이터 가져올 리스트 변수
        self.exitThread = False
        self.readThread(ser)

    def readThread(self, ser):              
            #데이터가 있있다면
        while not self.exitThread:
            for c in ser.read():
                #line 변수에 차곡차곡 추가하여 넣는다.
                self.line.append(chr(c))            
                if c == 10: #라인의 끝을 만나면..
                    #데이터 처리 함수로 호출
                    self.parsing_data(self.line)                
                    del self.line[:] #line 변수 초기화
    def parsing_data(self, data):
        # 리스트 구조로 들어 왔기 때문에
        # 작업하기 편하게 스트링으로 합침
        tmp = ''.join(data)    #출력!
        if "*" not in tmp: 
            msglist = tmp.split()
            msg = OpencrIMUSensor()
            msg.imu_time = int(msglist[0])
            msg.imu_roll = int(msglist[1])
            msg.imu_pitch = int(msglist[2]) 
            msg.imu_yaw = int(msglist[3])
            self.publisher_.publish(msg)

        self.get_logger().info(tmp)

    def handler(self,signum, frame):
     self.exitThread = True#데이터 처리할 함수

    # def timer_callback(self):
    #     msg = MockSensor()
    #     msg.sensor_id = "RAPA_SENSOR_1"
    #     msg.data = self.count
    #     self.publisher_.publish(msg)
    #     self.get_logger().info('Sensor ID: "%s", Data: "%d"' % (msg.sensor_id, msg.data))
    #     self.count += 1


def main(args=None):
    
    rclpy.init(args=args)
    custom_msg_publisher = CustomMsgPublisher()
    # signal.signal(signal.SIGINT, custom_msg_publisher.handler)    #시리얼 열기
    rclpy.spin(custom_msg_publisher)

    custom_msg_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()