import os
import numpy as np

class MidasConverter:
    """
    A class to convert OBJ files into MCT format for Midas software.
    """

    def __init__(self, work_dir):
        """
        Initializes the converter with necessary MCT template files.

        Args:
            work_dir (str): Directory where the mesh OBJ files are stored.
        """
        self._work_dir = work_dir
        self._header_content = self._load_template("header.mct")
        self._between_content = self._load_template("between.mct")
        self._back_content = self._load_template("back.mct")

        # Node management to ensure unique numbering
        self._mct_node_ids =  None
        self._mct_element_ids = None
        self._mct_groups = None

    def _load_template(self, file_name):
        """Loads the content of an MCT template file."""
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                return file.read()
        else:
            print(f"Warning: Template file '{file_name}' not found.")
            return ""


    def _convert_obj_to_mct_mesh(self, obj_file):
        """
        Converts an OBJ file to MCT format.

        Args:
            obj_file (str): Path to the OBJ file.

        Returns:
            tuple: (mct_nodes, mct_elements)
        """

        # Load mesh object
        nodes, elements = self._load_obj_as_mesh(obj_file)

        # Initialize and define start node
        mct_nodes = ""
        if self._mct_node_ids:
            start_node_id = self._mct_node_ids[-1] + 1
        else:
            start_node_id = 1
            self._mct_node_ids = []

        # Add nodes with unique IDs
        for idx, node in enumerate(nodes, start=start_node_id):
            mct_nodes += f"{idx}, {node[0]:.6f}, {node[1]:.6f}, {node[2]:.6f}\n"
            self._mct_node_ids.append(idx)

        # Set the startin element id checking attribute state
        mct_elements = ""
        if self._mct_element_ids:
            start_element_id = self._mct_element_ids[-1] + 1
        else:
            start_element_id = 1
            self._mct_element_ids = []

        # Add connectivity (mesh elements) to the text 
        for element_id, element_nodes in enumerate(elements, start=start_element_id):
            line_start = f"{element_id}, PLATE ,    1,     1,"
            self._mct_element_ids.append(element_id)
            if len(element_nodes) == 3:
                mct_elements += f"{line_start}  "
                for i in range(3):
                    mct_elements += f"{element_nodes[i] + start_node_id + 1}, "
                mct_elements += "0, 1, 0\n"
            elif len(element_nodes) == 4:
                mct_elements += f"{line_start}  "
                for i in range(4):
                    mct_elements += f"{element_nodes[i] + start_node_id + 1}, "
                mct_elements += "3, 0\n"
            else:
                print(f"Warning: Skipping unsupported face with {len(element_nodes)} vertices")

        # Save element groups
        group_dictionary = {
                'start_node_id': start_node_id,
                'end_node_id': self._mct_node_ids[-1],
                'start_element_id': start_element_id,
                'end_element_id': self._mct_element_ids[-1],
            }
        if self._mct_groups:
            self._mct_groups.append(group_dictionary)
        else:
            self._mct_groups = [group_dictionary]
        return mct_nodes, mct_elements


    def _convert_groups_to_mct(self):
        if self._mct_groups:
            mct_group_text = "*GROUP    ; Group\n"
            mct_group_text += "; NAME, NODE_LIST, ELEM_LIST, PLANE_TYPE\n"
            for group_id, group in enumerate(self._mct_groups, start=1):
                mct_group_text += f'Group{group_id}, {group["start_node_id"]}to{group["end_node_id"]}, '
                mct_group_text += f'{group["start_element_id"]}to{group["end_element_id"]}\n'
            mct_group_text += '\n'
            return mct_group_text
        else:
            return ""


    def _compose_mct_content(self, mct_nodes, mct_elements, mct_groups):
        """
        Composes the full MCT content from the given mesh data.

        Args:
            mct_nodes (str): Nodes section in MCT format.
            mct_elements (str): Elements section in MCT format.

        Returns:
            str: The generated MCT content as a string.
        """
        mct_content = self._header_content
        mct_content += mct_nodes
        mct_content += self._between_content
        mct_content += mct_elements
        mct_content += mct_groups
        mct_content += self._back_content
        return mct_content


    def write_all_meshes_into_one_mct(self, output_file):
        """
        Converts all OBJ files in the work directory into a single MCT file.

        Args:
            output_file (str): The final MCT file path.
        """
        print("\nMerging all OBJ files into one MCT file...")

        all_mct_nodes = ""
        all_mct_elements = ""
        self._mct_node_ids =  []
        self._mct_element_ids = []
        for file_name in os.listdir(self._work_dir):
            if file_name.endswith(".obj"):
                obj_file_path = os.path.join(self._work_dir, file_name)
                mct_nodes, mct_elements = self._convert_obj_to_mct_mesh(obj_file_path)
                all_mct_nodes += mct_nodes
                all_mct_elements += mct_elements
        mct_groups = self._convert_groups_to_mct()

        mct_content = self._compose_mct_content(all_mct_nodes, all_mct_elements, mct_groups)
        self.write_mct_file(output_file, mct_content)
        print(f"All meshes merged into: {output_file}")


    def write_all_meshes_separately(self):
        """
        Converts each OBJ file in the work directory into its own MCT file.
        """
        print("\nConverting all OBJ files separately...")

        for file_name in os.listdir(self._work_dir):
            if file_name.endswith(".obj"):
                obj_file_path = os.path.join(self._work_dir, file_name)
                mct_nodes, mct_elements = self._convert_obj_to_mct_mesh(obj_file_path)
                mct_content = self._compose_mct_content(mct_nodes, mct_elements, "")

                mct_file_path = os.path.join(self._work_dir, os.path.basename(obj_file_path).replace(".obj", ".mct"))
                self.write_mct_file(mct_file_path, mct_content)


    def write_mct_file(self, output_file_path, mct_content):
        with open(output_file_path, "w") as mct_file:
            mct_file.write(mct_content)
        print(f"MCT file saved: {output_file_path}")


    def _load_obj_as_mesh(self, file_path):
        """
        Reads an OBJ file and extracts nodes and element connectivity.

        Args:
            file_path (str): Path to the .obj file.

        Returns:
            nodes (np.ndarray): Array of (x, y, z) coordinates.
            elements (list of tuples): Connectivity of each element (tria or quad).
        """
        nodes = []
        elements = []

        with open(file_path, "r") as obj_file:
            for line in obj_file:
                parts = line.strip().split()
                if not parts:
                    continue

                # Read vertex data
                if parts[0] == "v":
                    nodes.append((float(parts[1]), float(parts[2]), float(parts[3])))

                # Read face data (1-based index in OBJ, so we subtract 1)
                elif parts[0] == "f":
                    face = [int(idx.split("/")[0]) - 1 for idx in parts[1:]]
                    elements.append(tuple(face))

        return np.array(nodes), elements


# Example Usage
if __name__ == "__main__":
    work_directory = "midas"
    converter = MidasConverter(work_directory)

    # Convert all OBJ files into separate MCT files
    # converter.write_all_meshes_separately()

    # Merge all OBJ files into one MCT file
    converter.write_all_meshes_into_one_mct("merged_output.mct")

# *GROUP    ; Group
# ; NAME, NODE_LIST, ELEM_LIST, PLANE_TYPE
#    appoggi   , 1to4, , 0
#    mezzo_shell, , 6 7, 0
#    lineaNodi1, 6 7 13, , 0
#    plate + nodi                           , 6 7 10to13, 8 9, 0
#    misto plate beam nodi ABCDEFGHIJKLMNOPQRSTUWXYVZ, 2 3 6 7 10to13, 3 4 7 8 9, 0
#    misto plate beam nodi ABCDEFGHIJKLMNOPQRSTUWXYVZ, 2 3 6 7 10to13, 3 4 8 9, 0
#    misto plate beam nodi ABCDEFGHIJKLMNOPQRSTUWXYVZ, 2 3 6 7 10to13, 3 4 8 9, 0
#    solo beam , , 3 4, 0
#    telaio NOME LUNGHISSIM0ABCDEFGHIJKLMNOPQRSTUWXYVZ    ,