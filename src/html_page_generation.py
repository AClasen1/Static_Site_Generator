import os
import block_transformation

def generate_page(from_path, template_path, dest_path):
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        from_file_text = from_file.read()
    with open(template_path) as template_file:
        template_file_text = template_file.read()
    from_file_title = block_transformation.extract_title(from_file_text)
    from_file_content = from_file_text #"\n".join(from_file_text.split("\n")[1:])
    from_file_content_html = block_transformation.markdown_to_html_node(from_file_content).to_html()
    templated_from_html = template_file_text.replace("""{{ Title }}""", from_file_title).replace("""{{ Content }}""", from_file_content_html)
    with open(dest_path, "w") as dest_file:
        if os.path.exists(os.path.dirname(dest_path)) == False:
            os.makedirs(os.path.dirname(dest_path))
        dest_file.write(templated_from_html)
        #print(templated_from_html)