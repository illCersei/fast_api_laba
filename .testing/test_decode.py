import base64

def decode_base64_to_image(base64_string, output_path):
    image_data = base64.b64decode(base64_string)
    with open(output_path, "wb") as output_file:
        output_file.write(image_data)

binary_base64 = ""

decode_base64_to_image(binary_base64, ".testing/binary_result.png")

print("DONE")
