def extract_sentences(input_list):
    extracted_sentences = []
    for text in input_list:
        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                extracted_sentences.append(line[1:].strip())
            elif line[:2].isdigit() and line[2] == '.':
                extracted_sentences.append(line[3:].strip())
    return extracted_sentences

def save_tasks_to_file(tasks_list, file_name):
    with open(file_name, "w") as file:
        for task in tasks_list:
            file.write(f"{task}\n")
        file.write("\n")

def main():
    input_data = [
        "Hello there\n- This is a test\n1. Example with numbers\n2. Another example\n- Final dash test",
        "- First dashed sentence\n- Second dashed sentence\n- Third one",
        "1. First numbered sentence\n2. Second numbered sentence\n3. Third numbered sentence",
        "Normal text with no bullet points\n- Valid dash entry\n1. Valid numbered entry\n3. Another valid number\nRandom text again",
        "-Single dash line\n1.Single numbered line",
        "  1.  Space before and after\n   - Irregular spacing for dashes\n \n2. Proper format but extra lines",
        "This is just a regular text without bullets.",
        "Introductory text\n1. Start of numbered points\n- Mixed dash\n2. Continue numbering\n- Another dash entry\nRandom trailing text"
    ]

    result = extract_sentences(input_data)
    print(result)
    output_file = "tasks_output.txt"
    save_tasks_to_file(result, output_file)

if __name__ == "__main__":
    main()
