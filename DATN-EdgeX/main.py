import csv
import re
import paho.mqtt.client as mqtt



def on_connect(client, userdata, flags, rc):  # Các hàm được gọi khi máy trạm kết nối với máy chủ nguồn cấp dữ liệu
    print("Connected with result code {0}".format(str(rc)))  # Hiển thị kết quả của lượt kết nối lên màn hình
    client.subscribe("huyquang")  # Đăng ký nhận thông báo từ kênh “digitest/test1” và nhận bất kỳ thông báo nào được phát đi từ kênh này


def on_message(client, userdata, msg):  # Hàm được gọi khi lệnh PUBLISH được gửi đến từ máy chủ.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Hiển thị thông báo được gửi 
    pattern = "\"name\"\:\"\w+\"\,\"value\"\:\"(?:-)?[0-9]+\""
    a = str(re.findall(pattern, str(msg.payload)))
    print(a)
    if a.find("humidity") > 0:
        x = str(re.findall("(?:-)?[0-9]+", a))
        x = x[2:-2]
        with open('./humidity.csv', 'a+', newline='') as f:
            employee_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([x])
            f.close()
        print(x)
    elif a.find("temperature") > 0:
        y = str(re.findall("(?:-)?[0-9]+", a))
        y = y[2:-2]
        with open('./temperature.csv', 'a+', newline='') as f:
            employee_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([y])
            f.close()
        print(y)


if __name__ == "__main__":
    client = mqtt.Client("digi_mqtt_test")  # Tạo phiên kết nối với máy trạm với mã nhận diễn máy trạm “digi_mqtt_test”
    client.on_connect = on_connect  # Định nghĩa hàm được gọi khi kết nối thành công Define callback function for successful connection
    client.on_message = on_message  # Định nghĩa hàm được gọi khi có thông báo xác nhận gửi đi thành công
    print(client.on_message)
    client.connect('broker.hivemq.com') 
   # client.connect("m2m.eclipse.org", 1883, 60)  # Kết nối tới (broker/máy chủ cấp dữ liệu, port/cổng kết nối, keepalive-time/thời gian giữ kết nối)
    client.loop_forever()  # Khởi động tiến trình mạng daemon
