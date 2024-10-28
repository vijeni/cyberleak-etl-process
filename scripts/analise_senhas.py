from zxcvbn import zxcvbn
import re

def avaliar_senha(senha):
  complexidade = ['Muito fraca', 'Fraca', 'Média', 'Forte', 'Muito forte']

  resultado = zxcvbn(senha)
  
  complexidade = complexidade[resultado['score']]
  avisos = resultado['feedback']['warning']
  tempo_adivinhacao = resultado['crack_times_display']['offline_slow_hashing_1e4_per_second']
  
  return complexidade, avisos, tempo_adivinhacao

def contabilizar_caracteres(senha):
  qntd_caract = len(senha)
  qntd_numeros = sum(c.isdigit() for c in senha)
  qntd_caract_text = sum(c.isalpha() for c in senha)
  qntd_caract_especiais = len(re.findall(r'[\W_]', senha))
  qntd_caract_text_upper = sum(c.isupper() for c in senha)
  qntd_caract_text_lower = sum(c.islower() for c in senha)
  return qntd_caract, qntd_caract_text, qntd_caract_especiais, qntd_numeros, qntd_caract_text_upper, qntd_caract_text_lower
