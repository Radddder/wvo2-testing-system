'''
ESP32_micropython mlx90640 @ Chengyu Xiao
'''
import machine  # type: ignore
import gc
import time
import mlx90640_v2
import micropython

print("Beginning main ...")
i2c = mlx90640_v2.I2C(pins=(5, 18), frequency=100000)
mlx = mlx90640_v2.MLX90640(i2c)
mlx.refresh_rate = mlx90640_v2.RefreshRate.REFRESH_0_5_HZ
frame = [0]*768

while True:
    
    gc.collect() 
    print("Querying camera ...\n")
    mlx.getFrame(frame)
    print(f"Frame received!")
          
    gc.collect()
    time.sleep(20.0)