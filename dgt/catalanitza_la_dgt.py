import pandas as pd
import ctranslate2
import pyonmttok
from huggingface_hub import snapshot_download
from tqdm import tqdm

# carrega el model de softcatalà
model_dir = snapshot_download(repo_id="softcatala/translate-spa-cat", revision="main")

tokenizer = pyonmttok.Tokenizer(mode="none", sp_model_path=model_dir + "/sp_m.model")
translator = ctranslate2.Translator(model_dir)

def translate_text(text):
    if not isinstance(text, str):
        return text
    tokens, _ = tokenizer.tokenize(text)
    translated = translator.translate_batch([tokens])
    return tokenizer.detokenize(translated[0][0]["tokens"])

# Si fos un programador de veritat i no un desgraciat, això hauria de ser un #TODO: Make an argparser out of it
df = pd.read_csv("preguntas_dgt.csv")

# Podriem fer servir [column_name].apply(translate_text) si tinguesim la GPU disponible... I si no tingués l'ànima morta
for i in tqdm(range(len(df)), desc="Translating"):
    for col in ["pregunta", "opcion_a", "opcion_b", "opcion_c"]:
        df.at[i, col] = translate_text(df.at[i, col])
df.to_csv("preguntas_dgt_cat.csv", index=False)
