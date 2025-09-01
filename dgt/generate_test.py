#!/usr/bin/env python3
"""
generate_test.py

Reads 'preguntas_dgt.csv' and outputs 'test.html':
 - one question per screen
 - smaller images
 - after answering, "Siguiente" button appears
"""

import csv
import json

INPUT_CSV = "preguntas_dgt.csv"
OUTPUT_HTML = "test.html"


def read_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            row = {k.strip(): (v.strip() if v else "") for k, v in r.items()}
            row["respuesta_correcta"] = row["respuesta_correcta"].lower()
            rows.append(row)
    return rows


def make_questions_json(rows):
    questions = []
    num_fail = 0
    for i, r in enumerate(rows, start=1):
        try:

            questions.append(
                {
                    "id": i,
                    "imagen": r["imagen"],
                    "pregunta": r["pregunta"].split('.')[1],
                    "opciones": {
                        "a": r["opcion_a"].split('A.')[1],
                        "b": r["opcion_b"].split('B.')[1],
                        "c": r["opcion_c"].split('C.')[1],
                    },
                    "correcta": r["respuesta_correcta"],
                }
            )
        except:
           print(r)
           num_fail += 1
    
    print(num_fail)
    return json.dumps(questions, ensure_ascii=False)


def generate_html(questions_json):
    html_template = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Test — Preguntas DGT</title>
<style>
  body { font-family: system-ui, sans-serif; background: #f6f7f8; margin: 0; }
  .wrap { max-width: 700px; margin: auto; padding: 16px; }
  .card { background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.08); padding: 16px; }
  .image-wrap { text-align:center; margin-bottom: 12px; }
  .image-wrap img { max-width: 80%; height: auto; max-height: 220px; border-radius: 8px; }
  .question-text { font-weight: 600; margin: 0 0 12px 0; }
  .options { display: flex; flex-direction: column; gap: 8px; }
  .opt-btn { border: 1px solid #ddd; border-radius: 8px; padding: 10px; background: #fff; text-align: left; cursor: pointer; }
  .opt-btn.correct { background: #e7f9ed; border-color: #34a853; }
  .opt-btn.incorrect { background: #fde7e9; border-color: #ea4335; }
  .feedback { margin-top: 10px; font-size: 0.9rem; }
  .feedback.correct { color: #0a7d31; }
  .feedback.incorrect { color: #b1001d; }
  .next-btn { margin-top: 14px; padding: 10px 14px; background: #0b7285; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; }
  .next-btn:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Test DGT — Práctica</h1>
  <div id="quiz"></div>
</div>

<script>
const QUESTIONS = __QUESTIONS_JSON__;

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

let index = 0;
let questions = shuffle(QUESTIONS);

function renderQuestion() {
  const q = questions[index];
  const quiz = document.getElementById('quiz');
  quiz.innerHTML = '';

  const card = document.createElement('div');
  card.className = 'card';

  const imgDiv = document.createElement('div');
  imgDiv.className = 'image-wrap';
  if (q.imagen) {
    const img = document.createElement('img');
    img.src = q.imagen;
    img.alt = 'Imagen pregunta';
    imgDiv.appendChild(img);
  }
  card.appendChild(imgDiv);

  const qText = document.createElement('p');
  qText.className = 'question-text';
  qText.textContent = (index+1) + '. ' + q.pregunta;
  card.appendChild(qText);

  const opts = document.createElement('div');
  opts.className = 'options';
  ['a','b','c'].forEach(letter => {
    const btn = document.createElement('button');
    btn.className = 'opt-btn';
    btn.textContent = letter.toUpperCase() + '. ' + q.opciones[letter];
    btn.addEventListener('click', () => {
      showFeedback(btn, opts, q, letter);
    });
    opts.appendChild(btn);
  });
  card.appendChild(opts);

  const feedback = document.createElement('div');
  feedback.className = 'feedback';
  feedback.style.display = 'none';
  card.appendChild(feedback);

  const nextBtn = document.createElement('button');
  nextBtn.className = 'next-btn';
  nextBtn.textContent = (index < questions.length-1) ? 'Siguiente →' : 'Finalizar';
  nextBtn.style.display = 'none';
  nextBtn.addEventListener('click', () => {
    if (index < questions.length-1) {
      index++;
      renderQuestion();
    } else {
      showEnd();
    }
  });
  card.appendChild(nextBtn);

  quiz.appendChild(card);
}

function showFeedback(clickedBtn, opts, q, chosen) {
  const correct = q.correcta;
  const feedback = opts.parentNode.querySelector('.feedback');
  const nextBtn = opts.parentNode.querySelector('.next-btn');

  opts.querySelectorAll('.opt-btn').forEach(btn => {
    btn.disabled = true;
    if (btn.textContent.startsWith(correct.toUpperCase() + '.')) {
      btn.classList.add('correct');
    }
    if (btn === clickedBtn && chosen !== correct) {
      btn.classList.add('incorrect');
    }
  });

  if (chosen === correct) {
    feedback.textContent = '✔ Correcto. La respuesta es ' + correct.toUpperCase() + '.';
    feedback.className = 'feedback correct';
  } else {
    feedback.textContent = '✘ Incorrecto. La correcta era ' + correct.toUpperCase() + '.';
    feedback.className = 'feedback incorrect';
  }
  feedback.style.display = 'block';
  nextBtn.style.display = 'inline-block';
}

function showEnd() {
  const quiz = document.getElementById('quiz');
  quiz.innerHTML = '<div class="card"><h2>Fin del test</h2><p>Has llegado al final.</p><button class="next-btn" onclick="restart()">Reiniciar</button></div>';
}

function restart() {
  index = 0;
  questions = shuffle(QUESTIONS);
  renderQuestion();
}

renderQuestion();
</script>
</body>
</html>
"""
    return html_template.replace("__QUESTIONS_JSON__", questions_json)


def main():
    rows = read_csv(INPUT_CSV)
    if not rows:
        print("CSV vacío o mal formado.")
        return
    questions_json = make_questions_json(rows)
    html = generate_html(questions_json)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✔ Archivo {OUTPUT_HTML} generado con {len(rows)} preguntas.")


if __name__ == "__main__":
    main()
