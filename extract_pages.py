from pypdf import PdfReader, PdfWriter
import pathlib
# page marked 1
START_PAGE = 15
END_PAGE = 694
INPUT_FILE = path = pathlib.Path('The C Programming Language 2nd.pdf')

with open('ignore.txt', 'r', encoding='utf-8') as f:
    ignore = f.read().splitlines()

if __name__ == '__main__':
    reader = PdfReader(INPUT_FILE)  # open input
    writer = PdfWriter()  # open output

    for page_num in range(START_PAGE - 1, END_PAGE):
        page = reader.pages[page_num]
        writer.add_page(page)

    print('Finished copying pages')

    with open("result" + INPUT_FILE.name, "wb") as fp:  # creating result pdf JCT
        writer.write(fp)  # writing to result pdf JCT
    print('Finished writing to file')
