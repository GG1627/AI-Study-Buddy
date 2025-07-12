import docx2txt

example_docx = "../data/Field_Assignment_2.docx"

doc_text = docx2txt.process(example_docx)

# Clean up the text
doc_text = doc_text.replace("\n", " ")
doc_text = doc_text.replace("\r", " ")
doc_text = doc_text.replace("\t", " ")
doc_text = doc_text.replace("\f", " ")
doc_text = doc_text.replace("\b", " ")
doc_text = doc_text.replace("\a", " ")
doc_text = doc_text.replace("\v", " ")

print(doc_text)








