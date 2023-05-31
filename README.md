# LLM-Pref-Mark-UI

This project provides a Gradio UI for marking preferences of human feedback on generated text. This could be used to train a reward model for RLHF.

There are two files, `app.py` for basic and `advanced_app.py` for advanced usage. Both are heavily inspired by Anthropic’s [“Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback”](https://arxiv.org/abs/2204.05862) paper.

NOTE: basic version is fully functioning except you have to fill in `record` function for your specific use case. That is how you would like to handle the clicks on chosen preferences. However, the advanced version is not fully functioning application. Instead, it provides only the UI.

### Basic version

<p align="center">
  <img src="https://i.ibb.co/Tcd3Dkd/2023-05-31-12-02-06.png" width="70%"/>
</p>

The basic version is demonstrated with Flan Alpaca model. All you need to do is the followings in `app.py`:

1. replace `model` variable with your own model
2. replace `GenerationConfig` with your own choice
3. complete `record()` function.
    - each choice on `A` and `B` is scored between 1 to 4
    - do whatever action you want with the scores

### Advanced version

<p align="center">
  <img src="https://i.ibb.co/Px2cHrc/2023-05-26-12-43-18-1.png" width="70%"/>
</p>
