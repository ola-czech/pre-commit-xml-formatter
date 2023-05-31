import argparse

from lxml import etree

def fix_file(filename: str, tab_width: int):
    with open(filename, 'rb') as reader:
        original_xml = reader.read()

    xml_parser = etree.XMLParser(remove_blank_text=True)
    parse_tree = etree.XML(original_xml, parser=xml_parser).getroottree()
    etree.indent(parse_tree, space=" " * tab_width)
    new_xml = etree.tostring(parse_tree,
                             pretty_print=True,
                             xml_declaration=True,
                             encoding=parse_tree.docinfo.encoding)
    if b'\r\n' in original_xml:
        new_xml = new_xml.replace(b'\n', b'\r\n')

    if new_xml != original_xml:
        print(f'Fixing {filename}')
        with open(filename, 'wb') as writer:
            writer.write(new_xml)


def main(args=None):
    current_filename = ''
    if args is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('filenames', nargs='*')
        parser.add_argument('--tab-width', type=int, default=4)
        args = parser.parse_args()
    try:
        for filename in args.filenames:
            current_filename = filename
            fix_file(filename, tab_width=args.tab_width)
        return 0
    except Exception as exc:
        print(current_filename)
        print(exc)
        return 1


if __name__ == '__main__':
    exit(main())