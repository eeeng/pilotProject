import spidev
import time
from RPi import GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)
from time import sleep
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=600000

#spi.max_speed_hz=25000
spi.lsbfirst=False
#spi.cshigh=False
#spi.cslow=True

spi.mode=0b01
spi.bits_per_word = 8


who_i_am=0x00
config1=0x01
config2=0X02
config3=0X03

reset=0x06
stop=0x0A
start=0x08
sdatac=0x11
rdatac=0x10
wakeup=0x02
rdata = 0x12

ch1set=0x05
ch2set=0x06
ch3set=0x07
ch4set=0x08
ch5set=0x09
ch6set=0x0A
ch7set=0x0B
ch8set=0x0C

data_test= 0x7FFFFF
data_check=0xFFFFFF

def read_byte(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 read_reg=spi.xfer(data)
# GPIO.output(18, True)
 print ("data", read_reg)

 
def send_command(command):
# GPIO.output(18, False)
 send_data = [command]
 com_reg=spi.xfer(send_data)
# GPIO.output(18, True)
# time.sleep(1)
 
def write_byte(register,data):
# GPIO.output(18, False)
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 print (data)
 spi.xfer(data)
# GPIO.output(18, True)
# time.sleep(1)

send_command (wakeup)
send_command (stop)
send_command (reset)
send_command (sdatac)


write_byte (0x14, 0x80) #GPIO
write_byte (config1, 0x96)
write_byte (config2, 0xD4)
write_byte (config3, 0xE0)
write_byte (0x04, 0x00)
#write_byte (0x0D, 0xFF)
write_byte (0x0E, 0x00)
write_byte (0x0F, 0x00)
write_byte (0x10, 0x00)
write_byte (0x11, 0x00)
write_byte (0x15, 0x20)
#
write_byte (0x17, 0x00)
write_byte (ch1set, 0x00)
write_byte (ch2set, 0x00)
write_byte (ch3set, 0x00)
write_byte (ch4set, 0x00)
write_byte (ch5set, 0x00)
write_byte (ch6set, 0x00)
write_byte (ch7set, 0x00)
write_byte (ch8set, 0x00)

send_command (rdatac)
send_command (start)
DRDY=1

result=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

while 1:
 GPIO.wait_for_edge(37, GPIO.FALLING)
 output=spi.readbytes(27)
 for a in range (3,25,3):
  voltage_1=(output[a]<<8)| output[a+1]
  voltage_1=(voltage_1<<8)| output[a+2]
  convert_voktage=voltage_1|data_test
  if convert_voktage==data_check:
   voltage_1_after_convert=(16777214-voltage_1)
  else:
   voltage_1_after_convert=voltage_1
  channel_num =  (a/3)
  result[int (channel_num)]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)
  print ("channel_num",channel_num, result[int (channel_num)])

spi.close()
print ("stop")


#time.sleep(0.1)