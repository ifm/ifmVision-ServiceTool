from xml.dom import minidom


class XMLParser(object):

    def __init__(self, file):
        self.file = file
        self.data = None

    def read_file(self):
        # Read recent.xml file
        with open(self.file, "r") as f:
            self.data = f.read()
        f.close()

    def write_data(self):
        try:
            root = minidom.Document()

            xml = root.createElement('root')
            root.appendChild(xml)

            xml_str = root.toprettyxml(indent="\t")

            with open(self.file, "w") as f:
                f.write(xml_str)
            f.close()
            return True
        except Exception as e:
            return e
