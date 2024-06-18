from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

# Set your Azure OpenAI endpoint and API key
endpoint = "https://<your-resource-name>.openai.azure.com/"
api_key = "your_azure_openai_api_key"

credential = AzureKeyCredential(api_key)
client = OpenAIClient(endpoint=endpoint, credential=credential)


#Definition to create prompt
def create_prompt(example_text, example_summary, input_text):
    example_paragraph = (
        example_text
    )
    example_summary = (
        example_summary
    )

    paragraph = (input_text)

    prompt = (
        f"Summarize the following paragraph. Here is an example:\n\n"
        f"Paragraph: {example_paragraph}\n"
        f"Summary: {example_summary}\n\n"
        f"Now, summarize the following paragraph:\n\n"
        f"Paragraph: {input_text}\n"
        f"Summary:"
    )
    return prompt

#Definition to chunk input input_text
def chunk_text(text, chunk_size):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

####
def summarize_chunk(chunk, client,exmple_input_text_for_prompt, exmple_input_summary_for_prompt):
    prompt = create_prompt(exmple_input_text_for_prompt, exmple_input_summary_for_prompt, chunk)
    response = client.completions.create(
        model="gpt-4-32k",
        prompt=prompt,
        temperature=0.5,

    )
    summary = response.choices[0].text.strip()
    return summary


############
def extract_summary(text, chunk_size=2000,exmple_input_text_for_prompt, exmple_input_summary_for_prompt):
    chunks = list(chunk_text(text, chunk_size))
    chunk_summaries = [summarize_chunk(chunk, client,exmple_input_text_for_prompt, exmple_input_summary_for_prompt) for chunk in chunks]
    combined_summary_text = " ".join(chunk_summaries)
    final_summary = summarize_chunk(combined_summary_text, client)
    return final_summary

# Example usage
exmple_input_text_for_prompt = "" #text from example excel
exmple_input_summary_for_prompt = "" #summary from example excel
input_text = ""  #input text from excel

summary = extract_summary(paragraph, chunk_size=2000 ,exmple_input_text_for_prompt, exmple_input_summary_for_prompt)
print("Summary:", summary)
