import time
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from devices.models import Device
from hengio.models import Hengio
from devices.models import Device
from auto.models import Auto
import os
import requests
import logging

# Thiết lập logger
logger = logging.getLogger(__name__)
def check_hengio_tasks():

    try:
        # Lấy thời gian hiện tại
        current_datetime = now()
        current_time = current_datetime.time()  # Lấy giờ và phút
        current_day = current_datetime.weekday()  # Lấy thứ trong tuần (0 = Thứ 2, 6 = Chủ Nhật)

        # Lọc các nhiệm vụ cần thực thi theo giờ và phút hiện tại
        hengios = Hengio.objects.filter(
            time__hour=current_time.hour,
            time__minute=current_time.minute
        )

        # # In ra các nhiệm vụ đã lọc được
        # if hengios.exists():
        #     print(f"Đã tìm thấy {hengios.count()} nhiệm vụ cần thực thi tại {current_time}:")
        #     for hengio in hengios:
        #         print(f" - {hengio.name}, Time: {hengio.time}, Days: {hengio.days_of_week}")
        # else:
        #     print(f"Không tìm thấy nhiệm vụ nào cần thực thi tại {current_time}.")

        # Kích hoạt nhiệm vụ
        for hengio in hengios:
            days_of_week_nums = [int(day) for day in hengio.days_of_week]
            if current_day in days_of_week_nums:
                print(f"Kích hoạt thiết bị: {hengio.name}")
                # Gửi yêu cầu HTTP đến thiết bị
                success = control_device(hengio.api_key, hengio.pin, hengio.status)
                if success:
                    print(f"Thiết bị '{hengio.name}' đã được cập nhật thành công.")
                else:
                    print(f"Lỗi: Không thể cập nhật thiết bị '{hengio.name}'.")
    except Exception as e:
        print(f"Lỗi trong check_hengio_tasks: {e}")


def check_and_control_system():
    """
    Kiểm tra và điều khiển hệ thống tự động.
    """
    try:
        auto = Auto.objects.filter(auto_status=Auto.ON).first()
        if not auto:
            print("Không có Auto nào đang hoạt động.")
            return
        if auto.pump_choice == Auto.CONTINUOUS:
            print("Bơm liên tục đang bật.")
            control_device(auto.api_key, auto.pump_pin, 1)
        control_ph(auto)
        control_light(auto)

    except Exception as e:
        print(f"Lỗi trong check_and_control_system: {e}")


def control_ph(auto):
    """
    Kiểm tra giá trị pH và điều khiển van xả thấp, xả cao. 
    Mở van dưỡng chất nếu van xả được mở và van_status = ON.
    """
    # Lấy thiết bị đo giá trị pH
    current_ph_device = Device.objects.filter(pin=auto.vanph_pin).first()
    if not current_ph_device:
        print("Không tìm thấy thiết bị đo giá trị pH.")
        return

    try:
        # Chuyển đổi giá trị pH
        current_ph = float(current_ph_device.value)
        min_ph = float(auto.min_ph)
        max_ph = float(auto.max_ph)

        print(f"pH hiện tại: {current_ph}, min_ph: {min_ph}, max_ph: {max_ph}")

        if current_ph < min_ph:
            # Mở van xả thấp
            print("Mở van xả thấp (vanph_min_pin).")
            control_device(auto.api_key, auto.vanph_min_pin, 1)

            # Kiểm tra van_status để mở dưỡng chất
            if auto.van_status == Auto.ON:
                print("Van chính đang mở, kích hoạt dưỡng chất.")
                control_device(auto.api_key, auto.duong_chat_1, 1)
                control_device(auto.api_key, auto.duong_chat_2, 1)

        elif current_ph > max_ph:
            # Mở van xả cao
            print("Mở van xả cao (vanph_max_pin).")
            control_device(auto.api_key, auto.vanph_max_pin, 1)

            # Kiểm tra van_status để mở dưỡng chất
            if auto.van_status == Auto.ON:
                print("Van chính đang mở, kích hoạt dưỡng chất.")
                control_device(auto.api_key, auto.duong_chat_1, 1)
                control_device(auto.api_key, auto.duong_chat_2, 1)

        else:
            # Đóng tất cả các van
            print("pH trong giới hạn an toàn, đóng tất cả van.")
            control_device(auto.api_key, auto.vanph_min_pin, 0)
            control_device(auto.api_key, auto.vanph_max_pin, 0)
            control_device(auto.api_key, auto.duong_chat_1, 0)
            control_device(auto.api_key, auto.duong_chat_2, 0)

    except ValueError:
        print("Giá trị pH không hợp lệ.")

def control_light(auto):
    """
    Kiểm tra và điều khiển ánh sáng.
    """
    light_device = Device.objects.filter(pin=auto.light_pin).first()
    if not light_device:
        print("Không tìm thấy thiết bị ánh sáng.")
        return

    try:
        current_light = float(light_device.value)
        min_light = float(auto.min_light)

        if current_light < min_light:
            print("Bật ánh sáng.")
            control_device(auto.api_key, auto.light_relay, 1)
        else:
            print("Tắt ánh sáng.")
            control_device(auto.api_key, auto.light_relay, 0)

    except ValueError:
        print("Giá trị ánh sáng không hợp lệ.")
def control_pump_job():
    """
    Điều khiển bơm định kỳ ở chế độ ngắt quãng.
    Nếu trạng thái bơm là 0 thì chuyển thành 1 và ngược lại.
    """
    try:
        # Lấy Auto đang hoạt động
        auto = Auto.objects.filter(auto_status=Auto.ON).first()
        if not auto:
            print("Không có Auto nào đang hoạt động.")
            return

        # Kiểm tra nếu bơm đang ở chế độ ngắt quãng
        if auto.pump_choice == Auto.INTERVAL:
            print("Kiểm tra trạng thái bơm cho chế độ ngắt quãng.")
            
            # Lấy thiết bị bơm dựa trên pump_pin
            pump_device = Device.objects.filter(pin=auto.pump_pin).first()
            if not pump_device:
                print(f"Không tìm thấy thiết bị bơm với pin {auto.pump_pin}.")
                return

            # Lấy giá trị hiện tại của bơm
            try:
                current_value = int(pump_device.value)
            except ValueError:
                print(f"Giá trị hiện tại của bơm ({pump_device.value}) không hợp lệ.")
                return

            # Chuyển đổi trạng thái bơm
            new_value = 1 if current_value == 0 else 0
            print(f"Chuyển bơm từ {current_value} thành {new_value}.")
            control_device(auto.api_key, auto.pump_pin, new_value)

    except Exception as e:
        print(f"Lỗi trong control_pump_job: {e}")

def control_device(api_key, pin, value):

    device_ip = os.environ.get('HOST', '')

    # if not device_ip:
    #     print("Không tìm thấy giá trị HOST trong biến môi trường hoặc biến môi trường chưa được đặt.")
    #     return False

    #url = f'http://{device_ip}:8000/update/{api_key}/{pin}/?value={value}'
    url = f'http://103.252.136.73:8000/update/{api_key}/{pin}/?value={value}'
    print(url)
    response = requests.get(url)
    return response.status_code == 200