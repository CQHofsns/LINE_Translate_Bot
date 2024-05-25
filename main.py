#from translate_model import translate_engine
from googletrans import Translator
import time

start= time.time()
message= "<2en> Bây giờ tôi muốn phân công việc này thành các task nhỏ hơn và chia cho Long, Shikada, và Yu. Mọi người nghĩ sao về cách phân công này"
#output= translate_engine.run(message= message)
translator= Translator()
output= translator.translate(message, dest= "ja", src= "vi")
print(output)

print(round(time.time()- start))