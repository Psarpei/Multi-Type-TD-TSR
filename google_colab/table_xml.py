from lxml import etree

def output_to_xml(table_coords, list_table_boxes):
    root = etree.Element("page")

    for i in range(len(list_table_boxes)):
        table = etree.SubElement(root, "table")
        bbox = etree.SubElement(table, "boundingbox")
        bbox.attrib["x"] = str(table_coords[i][0])
        bbox.attrib["y"] = str(table_coords[i][1])
        bbox.attrib["w"] = str(table_coords[i][2])
        bbox.attrib["h"] = str(table_coords[i][3])
        start_x = table_coords[i][0]
        start_y = table_coords[i][1]

        for j in range(len(list_table_boxes[i])):
            for k in range(len(list_table_boxes[i][j])):

                cell = etree.SubElement(table, "cell")
                cell.attrib["row"] = str(j)
                cell.attrib["column"] = str(k)
                bbox = etree.SubElement(cell, "boundingbox")
                bbox.attrib["x"] = str(start_x + list_table_boxes[i][j][k][0][0])
                bbox.attrib["y"] = str(start_y + list_table_boxes[i][j][k][0][1])
                bbox.attrib["w"] = str(list_table_boxes[i][j][k][0][2])
                bbox.attrib["h"] = str(list_table_boxes[i][j][k][0][3])
                #print("table:",i, " row", j, " column:", k, "boundingbox", list_table_boxes[i][j][k])

    et = etree.ElementTree(root)
    et.write('output.xml', pretty_print=True)
