from lxml import etree


def output_to_xml(list_table_boxes, output_path):
    root = etree.Element("table")
    for j in range(len(list_table_boxes)):
        for k in range(len(list_table_boxes[0])):
            if(list_table_boxes[j][k] != []):
                cell = etree.SubElement(root, "cell")
                cell.attrib["row"] = str(j)
                cell.attrib["column"] = str(k)
                bbox = etree.SubElement(cell, "boundingbox")
                bbox.attrib["x"] = str(list_table_boxes[j][k][0][0])
                bbox.attrib["y"] = str(list_table_boxes[j][k][0][1])
                bbox.attrib["w"] = str(list_table_boxes[j][k][0][2])
                bbox.attrib["h"] = str(list_table_boxes[j][k][0][3])

    et = etree.ElementTree(root)
    et.write(output_path + "xml", pretty_print=True)
