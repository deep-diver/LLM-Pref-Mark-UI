import gradio as gr
from styles import BASIC_STYLE
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, GenerationConfig

model_id = "declare-lab/flan-alpaca-large"
torch_device = "cuda" if torch.cuda.is_available() else "cpu"

if torch_device == "cuda":
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id, load_in_8bit=True, device_map="auto")
else:
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)
generation_config = GenerationConfig.from_pretrained(model_id)
generation_config.do_sample = True

pref_btns = []

def record(btn):
  # scale 1 to 4
  score = len(btn)

  if "A" in btn:
    # record in DB
    print(f"A on score of {score}")
  else:
    # in case of "B"
    # record in DB
    print(f"B on score of {score}")

def generate(prompt):
  model_inputs = tokenizer([prompt, prompt], return_tensors="pt").to(torch_device)
  generated_ids = model.generate(
      **model_inputs,
      generation_config=generation_config,
  )
  decoded = tokenizer.batch_decode(
      generated_ids, skip_prompt=True, skip_special_tokens=True
  )

  return (
      decoded[0],
      decoded[1]
  )

with gr.Blocks(css=BASIC_STYLE, theme='gradio/soft') as demo:
  score = gr.State()

  with gr.Column(elem_id="col-container"):
    gr.Markdown(
        "# Marking preference of responses generated by SFT model",
        elem_id="top-title"
    )
    gr.Markdown(
        "The recorded preferences will be used to train a reward model for the RLHF"
    )

    prompt = gr.Textbox(
        label="", elem_id="prompt-txt-input", placeholder="Enter an instruction"
      )

    with gr.Row(elem_id="middle"):
      with gr.Column(elem_id="middle-right"):
        gr.Markdown("### Choose the most helpful and honest response from the current turn of conversation", elem_id="middle-title")

        a_res = gr.Textbox(
            "",
            lines=15,
            label="A"
        )
        b_res = gr.Textbox(
            "",
            lines=15,
            label="B"
        )

        with gr.Row(elem_id="middle-right-bottom"):
            for i in range(1, 9):
              letter = "A" if i < 5 else "B"
              spaces = (" " * (4-i)) if i < 5 else (" " * (i-5))
              btn_label = f"{letter}{spaces}"

              btn = gr.Button(btn_label, interactive=False, elem_id=f"res-pref-{i}-btn")
              pref_btns.append(btn)

    prompt.submit(
        generate,
        prompt,
        [a_res, b_res]
    ).then(
        lambda: [
            gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True),
            gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True),
        ],
        None,
        pref_btns
    )

    for pref_btn in pref_btns:
      pref_btn.click(
          lambda: [
              gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False),
              gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False),
          ],
          None,
          pref_btns
      ).then(
          lambda: ["", "", ""],
          None, 
          [prompt, a_res, b_res]
      ).then(
          record,
          pref_btn,
          None
      )

demo.queue().launch()
