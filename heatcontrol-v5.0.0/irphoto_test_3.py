from mlx90640_v4 import I2C, MLX90640, RefreshRate, __memory_manage

#### Main Program ####
print("Beginning main ...")
gc.threshold(5000) # Seriously push the memory managing to the limit! Manages every <n> bytes allocated
 
ixc = I2C(pins=(5, 18), frequency=100000)
mlx = MLX90640(ixc)
mlx.refresh_rate = RefreshRate.REFRESH_0_5_HZ
frame = [0]*768

print("Querying camera ...\n")
while(1):
    mlx.getFrame(frame)
    print(frame)
    print("\n")
    __memory_manage()