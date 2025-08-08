from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = 'google/flan-t5-small'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

print("Model and tokenizer downloaded successfully!")
