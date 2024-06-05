from autoannot import convert_annotation

if __name__ == "__main__":

    import argparse
    from pathlib import Path
    import os
    import re

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="path to input directory")
    parser.add_argument("-o", "--output", type=str, required=False, default="",
                        help="path to output directory, if not provided it will create a sister directory"
                             "with same name as the input directory but with suffix '_<extension name>")
    parser.add_argument("-t", "--to", type=str, required=False, default="TextGrid",
                        help="extension to convert to")

    args = parser.parse_args()

    # Input directory
    input_dir = Path(args.input)
    if not input_dir.exists():
        raise FileNotFoundError(f"'input_dir' == '{input_dir}' does not exist")

    # Target file type: CSV or TextGrid
    to = args.to
    if to not in ["csv", "CSV", "textgrid", "TextGrid"]:
        raise ValueError(f"'to' == '{to}' is not a valid extension")

    # Output directory
    if args.output == "":
        output_dir = input_dir.parent / f"{args.input}_{to}"
    else:
        output_dir = Path(args.output)

    if not output_dir.exists():
        os.makedirs(output_dir)

    for file in os.listdir(input_dir):

        match = re.match(r"([\w\-_.]+)\.(csv|CSV|textgrid|TextGrid)", file)
        if not match:
            print(f"Skipping {file}")
            continue

        stem = match.group(1)
        convert_annotation(in_file=input_dir / file, out_file=output_dir / f"{stem}.{to}")
