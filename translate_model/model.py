import torch

from langdetect import detect
from transformers import T5ForConditionalGeneration, T5Tokenizer

class Translate_Model:
    def __init__(self, cache_dir) -> None: 
        device= "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer= T5Tokenizer.from_pretrained(
            pretrained_model_name_or_path= "jbochi/madlad400-3b-mt",
            cache_dir= cache_dir
        )

        self.model= T5ForConditionalGeneration.from_pretrained(
            pretrained_model_name_or_path= "jbochi/madlad400-3b-mt",
            cache_dir= cache_dir,
            device_map= "auto"
        )

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
        
    def run(self, message):
        inputs= self.tokenizer(text= message, return_tensors= "pt").input_ids.to(self.model.device)

        translated_tokens= self.model.generate(
            input_ids= inputs,
            max_length= 128,
            num_beams= 2,
            no_repeat_ngram_size= 2,
            early_stopping= True
        )

        return self.tokenizer.decode(translated_tokens[0], skip_special_tokens= True)
    

