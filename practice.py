import time
from datetime import datetime
from plyer import notification

while True:
    # 현재 시간 체크
    current_time = datetime.now().strftime('%H:%M')
    
    # 14:40에 알림 보내기
    if current_time == "10:17":
        notification.notify(
            title='Backtest Reminder',
            message='It\'s time for the backtest!',
            app_icon=None,  
            timeout=10,
        )
        time.sleep(60)  # 알림 후 1분 동안 대기 (중복 알림 방지)
    time.sleep(10)  # 10초마다 시간 체크
