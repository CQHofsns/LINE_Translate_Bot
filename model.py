import os
import sys
import torch

from langdetect import detect
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

sys.path.append(".")

class Translate_Model:
    def __init__(self) -> None: 
        device= "cuda" if torch.cuda.is_available() else "cpu"
        self.model= AutoModelForSeq2SeqLM.from_pretrained(
            pretrained_model_name_or_path= "facebook/nllb-200-distilled-600M",
            cache_dir= os.path.join("cache_dir/")
        )

        self.model.to(device)

    def _langdetect(self, message):
        lang_dict= {
            "vi": "vie_Latn",
            "en": "eng_Latn",
            "ja": "jpn_Jpan",
            "zh-cn": "zho_Hans" ,
            "zh-tw": "zho_Hant"
        }
        detlang= detect(text= message)
        
        if detlang:
            return lang_dict[detlang]
        else:
            raise SystemError("Invalid language detected, contact Admin to update new language")
        
    def run(self, message, target_lang):
        lang_code= self._langdetect(message= message)

        self.tokenizer= AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path= "facebook/nllb-200-distilled-600M",
            src_lang= lang_code,
            cache_dir= os.path.join("cache_dir/")
        )

        inputs= self.tokenizer(text= message, return_tensors= "pt")

        translated_tokens= self.model.generate(
            **inputs, forced_bos_token_id= self.tokenizer.lang_code_to_id[target_lang],
            max_length= len(message.split())
        )

        return self.tokenizer.batch_decode(translated_tokens, skip_special_tokens= True)[0]
    
message= "Bây giờ tôi muốn phân công việc này thành các task nhỏ hơn và chia cho Long, Shikada, và Yu. Mọi người làm đến dâu rồi?"
output= Translate_Model().run(message= message, target_lang= "eng_Latn")

print(output)
